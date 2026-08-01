#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""YouTube の再生リストから全動画 URL を取得する。

yt-dlp (stable / nightly とも) は WEB クライアント経由で取りにいくが、
Shorts の再生リストは richGrid レイアウトで返り、その continuation を
YouTube が空レスポンスで弾くため 1 ページ目 (100 件) で止まってしまう。

このスクリプトは InnerTube API を TVHTML5 クライアントで叩く。
TVHTML5 は tileRenderer + 旧形式の nextContinuationData を返し、
こちらは continuation が普通に通るので最後まで辿れる。

usage:
    python fetch_playlist.py <playlist_url_or_id> [options]

options:
    -o, --output FILE   ファイルに書き出す (既定は標準出力)
    --json              `  "url",` 形式で出す (index.html の VIDEOS に貼る用)
    --shorts            /shorts/<id> 形式の URL にする (既定は /watch?v=)
    --client NAME       TVHTML5 (既定) / WEB
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request

INNERTUBE_URL = "https://www.youtube.com/youtubei/v1/browse"
INNERTUBE_KEY = "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"  # 公開されている WEB 用キー
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

CLIENTS = {
    # name: (X-Youtube-Client-Name, clientVersion)
    "TVHTML5": ("7", "7.20240304.10.00"),
    "WEB": ("1", "2.20240304.00.00"),
}


def extract_playlist_id(s):
    m = re.search(r"[?&]list=([A-Za-z0-9_-]+)", s)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]+", s):
        return s
    raise SystemExit("playlist ID を取り出せません: %s" % s)


def post(body, client):
    num, ver = CLIENTS[client]
    req = urllib.request.Request(
        INNERTUBE_URL + "?key=" + INNERTUBE_KEY + "&prettyPrint=false",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": UA,
            "X-Youtube-Client-Name": num,
            "X-Youtube-Client-Version": ver,
            "Origin": "https://www.youtube.com",
            "Accept-Language": "en-US,en;q=0.9",
        },
        method="POST",
    )
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
            time.sleep(1 + attempt)
    raise SystemExit("InnerTube へのリクエストに失敗: %s" % last)


def context(client):
    return {"client": {"clientName": client, "clientVersion": CLIENTS[client][1],
                       "hl": "en", "gl": "US"}}


def scan(node, videos, seen, tokens):
    """レスポンスを再帰的に歩いて動画 ID と continuation token を拾う。

    クライアントごとにレイアウトが違う (TVHTML5=tileRenderer,
    WEB=playlistVideoRenderer / shortsLockupViewModel) ので、
    決め打ちのパスは使わず全部見る。
    """
    if isinstance(node, dict):
        # TVHTML5
        t = node.get("tileRenderer")
        if isinstance(t, dict):
            vid = (t.get("contentId")
                   or t.get("onSelectCommand", {}).get("watchEndpoint", {}).get("videoId"))
            _add(videos, seen, vid)

        # WEB (通常動画)
        vr = node.get("playlistVideoRenderer")
        if isinstance(vr, dict):
            _add(videos, seen, vr.get("videoId"))

        # WEB (Shorts)
        sl = node.get("shortsLockupViewModel")
        if isinstance(sl, dict):
            _add(videos, seen, sl.get("onTap", {}).get("innertubeCommand", {})
                                 .get("reelWatchEndpoint", {}).get("videoId"))

        # continuation: 旧形式と新形式の両方
        nc = node.get("nextContinuationData")
        if isinstance(nc, dict) and nc.get("continuation"):
            tokens.append(nc["continuation"])
        cc = node.get("continuationCommand")
        if isinstance(cc, dict) and cc.get("token"):
            tokens.append(cc["token"])

        for v in node.values():
            scan(v, videos, seen, tokens)
    elif isinstance(node, list):
        for v in node:
            scan(v, videos, seen, tokens)


def _add(videos, seen, vid):
    if vid and vid not in seen:
        seen.add(vid)
        videos.append(vid)


def fetch_all(playlist_id, client="TVHTML5", verbose=True, max_pages=500):
    videos, seen = [], set()
    body = {"context": context(client), "browseId": "VL" + playlist_id}
    for page in range(1, max_pages + 1):
        data = post(body, client)
        tokens, before = [], len(videos)
        scan(data, videos, seen, tokens)
        if verbose:
            print("page %d: +%d (total %d)" % (page, len(videos) - before, len(videos)),
                  file=sys.stderr)
        # token が無い / 新規 0 件なら打ち止め
        if not tokens or len(videos) == before:
            break
        body = {"context": context(client), "continuation": tokens[0]}
    return videos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("playlist", help="再生リストの URL か ID")
    ap.add_argument("-o", "--output")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--shorts", action="store_true")
    ap.add_argument("--client", default="TVHTML5", choices=sorted(CLIENTS))
    args = ap.parse_args()

    ids = fetch_all(extract_playlist_id(args.playlist), client=args.client)
    print("取得: %d 件" % len(ids), file=sys.stderr)

    base = "https://www.youtube.com/shorts/" if args.shorts \
        else "https://www.youtube.com/watch?v="
    urls = [base + i for i in ids]
    lines = ['  "%s",' % u for u in urls] if args.json else urls
    out = "\n".join(lines) + "\n"

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fp:
            fp.write(out)
        print("書き出し: %s" % args.output, file=sys.stderr)
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
