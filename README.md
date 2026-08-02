# playlist1
YouTube のリスト機能は以下の点で不便なので自作する:

- 不便1: シャッフル再生をしても偏りがある
- 不便2: 200件以上を表示できない

## 自作したもの
- プレイリスト例: https://www.youtube.com/playlist?list=PLe-53kFdap50mj3afosEvQHVCeoEYuDgP
- 自作プレイリスト: https://stakiran.github.io/playlist1/

<img width="1623" height="807" alt="Image" src="https://github.com/user-attachments/assets/24de6598-a533-4a5f-8edb-8a79e235aa33" />

## 技術
Try2 参照.

## 自動更新
🔒️<https://claude.ai/chat/aa01617c-cc95-4a3a-af63-5b86b1e53c79>

claude.ai の予定済みタスクにしようとしたけど、youtube.com に行けないみたいなので gh_actions 式になった。

60日制限:

> これで仕込みは完了です。次回からは毎週日曜 5:00 JST 前後(cron の混雑次第で多少遅れます)に自動実行され、新着がなければ「変更なし」で commit せずに終わります。あとは放置でOKですが、60日間リポジトリに活動がないと scheduled workflow が停止する点だけ頭の片隅に置いておいてください(停止時は GitHub からメールが来ます)。
