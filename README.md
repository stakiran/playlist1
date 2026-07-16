# playlist1
YouTube の再生リストは出来が悪いので Fable 5 につくってもらった。

🔒️ <https://claude.ai/chat/5fff46a7-09cd-419e-ab6d-167b053d3e54>

出来が悪い点:

- ランダム再生:
    - ランダムに偏りがありすぎるし、20？くらい見てると止まってそれ以上見れなくなる

## URL 一覧の取得
> 再生リストのURLから全動画のURLを一括で抜き出したい場合は、yt-dlpで yt-dlp --flat-playlist --print url "再生リストURL" とすれば一覧が取れるので、それを配列に貼り付けるのが楽です。

"D:\download\yt-dlp.exe" --flat-playlist --print url  "https://www.youtube.com/watch?v=29bkUlxPOVU&list=PLe-53kFdap50mj3afosEvQHVCeoEYuDgP"

> --print のテンプレートに配列の書式ごと埋め込めます。JSON形式で安全にクォートしてくれる %(...)j を使うのがコツです。

"D:\download\yt-dlp.exe" --flat-playlist --print "  %(url)j," "https://www.youtube.com/watch?v=29bkUlxPOVU&list=PLe-53kFdap50mj3afosEvQHVCeoEYuDgP"

"D:\download\yt-dlp.exe" --flat-playlist --print "  %(url)j," "https://www.youtube.com/watch?v=29bkUlxPOVU&list=PLe-53kFdap50mj3afosEvQHVCeoEYuDgP" > urls.txt

## ローカルで見る

```
$ python3 -m http.server
$ http://localhost:8000/
```
