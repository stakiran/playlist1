#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""再生リストを取得し、index.html の VIDEOS に未反映分を追記する。

- fetch_playlist.py の fetch_all() を使って全件取得 (TVHTML5)
- index.html の VIDEOS ブロックに無い動画 ID だけを末尾に追記
  (手動で並べ替えたり { url, title } 形式にした既存行は触らない)
- urls.txt は取得結果の全件で書き直す

変更が無ければ何もしない。GitHub Actions 側は git diff で commit 要否を判断する。
"""

import re
import sys

from fetch_playlist import fetch_all

PLAYLIST_ID = "PLe-53kFdap50mj3afosEvQHVCeoEYuDgP"
INDEX_HTML = "index.html"
URLS_TXT = "urls.txt"
URL_BASE = "https://www.youtube.com/shorts/"

ID_RE = re.compile(r"(?:v=|youtu\.be/|embed/|shorts/)([\w-]{11})")


def main():
    ids = fetch_all(PLAYLIST_ID)
    if not ids:
        # 取得 0 件は API 側の異常とみなし、既存データを壊さないよう中断
        raise SystemExit("取得 0 件のため中断 (index.html は変更しない)")
    print("取得: %d 件" % len(ids), file=sys.stderr)

    with open(INDEX_HTML, encoding="utf-8") as fp:
        html = fp.read()

    m = re.search(r"const VIDEOS = \[\n(.*?)\n(\];)", html, re.S)
    if not m:
        raise SystemExit("index.html に VIDEOS ブロックが見つかりません")
    block = m.group(1)
    existing = set(ID_RE.findall(block))
    print("index.html 内: %d 件" % len(existing), file=sys.stderr)

    new_ids = [i for i in ids if i not in existing]
    if new_ids:
        add_lines = "".join('  "%s%s",\n' % (URL_BASE, i) for i in new_ids)
        html = html[:m.start(2)] + add_lines + html[m.start(2):]
        with open(INDEX_HTML, "w", encoding="utf-8") as fp:
            fp.write(html)
        print("index.html に %d 件追記" % len(new_ids), file=sys.stderr)
        for i in new_ids:
            print("  + %s%s" % (URL_BASE, i), file=sys.stderr)
    else:
        print("追記なし (すべて反映済み)", file=sys.stderr)

    # urls.txt は fetch_playlist.py --json --shorts と同じ形式で全件書き直す
    out = "".join('  "%s%s",\n' % (URL_BASE, i) for i in ids)
    with open(URLS_TXT, "w", encoding="utf-8") as fp:
        fp.write(out)


if __name__ == "__main__":
    main()
