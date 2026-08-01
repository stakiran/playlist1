YouTube の再生リストは出来が悪いので Fable 5 につくってもらった。

🔒️ <https://claude.ai/chat/5fff46a7-09cd-419e-ab6d-167b053d3e54>

出来が悪い点:

- ランダム再生:
    - ランダムに偏りがありすぎるし、20？くらい見てると止まってそれ以上見れなくなる

## URL 一覧の取得
> 再生リストのURLから全動画のURLを一括で抜き出したい場合は、yt-dlpで yt-dlp --flat-playlist --print url "再生リストURL" とすれば一覧が取れるので、それを配列に貼り付けるのが楽です。

```
"D:\download\yt-dlp.exe" --flat-playlist --print url  "https://www.youtube.com/watch?v=29bkUlxPOVU&list=PLe-53kFdap50mj3afosEvQHVCeoEYuDgP"
```

> --print のテンプレートに配列の書式ごと埋め込めます。JSON形式で安全にクォートしてくれる %(...)j を使うのがコツです。

```
"D:\download\yt-dlp.exe" --flat-playlist --print "  %(url)j," "https://www.youtube.com/watch?v=29bkUlxPOVU&list=PLe-53kFdap50mj3afosEvQHVCeoEYuDgP"
```

```
"D:\download\yt-dlp.exe" --flat-playlist --print "  %(url)j," "https://www.youtube.com/watch?v=29bkUlxPOVU&list=PLe-53kFdap50mj3afosEvQHVCeoEYuDgP" > urls.txt
```

> 101という数字がヒントです。YouTubeはプレイリストを100件ずつのページに分けて返しており、yt-dlpが2ページ目以降（continuation）の取得に失敗すると、ちょうど1ページ分＋再生中の1本＝101本で止まります。よくある原因と対処は次の2つです。

```
"D:\download\yt-dlp.exe" --flat-playlist --print "  %(url)j," "https://www.youtube.com/playlist?list=PLe-53kFdap50mj3afosEvQHVCeoEYuDgP" > urls.txt
```

> 2026年6月に「プレイリストが100〜120件しか取得できない」というまさに同じ症状のissueが報告されており、932本のリストで最初の120件しか取れない、121件目を直接指定すると0件になる、という内容です。修正PR（#16948「Fix pagination」）はマージ済みですが、YouTube側の変更は頻繁で、stable版に反映が追いついていないことがあります。 
> 
> 1. nightly版に切り替える（一番効く可能性が高い） stable は最新でも、修正が先に入るのは nightly です：

```
"D:\download\yt-dlp-nightly.exe" --flat-playlist --print "  %(url)j," "https://www.youtube.com/playlist?list=PLe-53kFdap50mj3afosEvQHVCeoEYuDgP" > urls.txt
```

🐰変わらん。。。  at 2026-07-17 07:33:43
