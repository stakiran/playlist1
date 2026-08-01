# リベンジ
try1 のが再現性があった → InnerTube API → 同じ問題 → なんかどうやったら pagenation 取れるか延々調べてるな…… → TVHTML5 client が正解とのこと

# 🤖

## URL 一覧の取得

`fetch_playlist.py` で全件取れる（依存ライブラリなし、標準ライブラリのみ）。

```
$ python fetch_playlist.py "https://www.youtube.com/playlist?list=PLe-53kFdap50mj3afosEvQHVCeoEYuDgP" --json --shorts -o urls.txt
page 1: +15 (total 15)
...
page 18: +15 (total 270)
取得: 270 件
```

- `--json` … `  "url",` 形式で出す（index.html の `VIDEOS` にそのまま貼れる）
- `--shorts` … `/shorts/<id>` 形式にする（既定は `/watch?v=`）
- `--client WEB` … 比較用。101 件で止まるのが確認できる

### yt-dlp が 101 件で止まっていた理由

yt-dlp は stable / nightly とも 101 件で止まる（`playlist_count` は 270 と正しく報告する）。

- この再生リストは **Shorts の再生リスト**で、WEB クライアントだと
  `richGrid` + `shortsLockupViewModel` というレイアウトで返ってくる
- その continuation token を投げると YouTube が
  `{"responseContext":..., "trackingParams":...}` だけの**空レスポンス**を返して弾く
  （visitorData を固定しても駄目だった）
- つまり pagination 修正 PR (#16948) とは別件で、Shorts playlist 側の問題

**TVHTML5 クライアント**（テレビ向け）で InnerTube API を叩くと
`tileRenderer` + 旧形式の `nextContinuationData` で返ってきて、
こちらは continuation が普通に通る。15 件 × 18 ページで 270 件 全部取れる。

# ローカルで見る

```
$ python3 -m http.server
$ http://localhost:8000/
```
