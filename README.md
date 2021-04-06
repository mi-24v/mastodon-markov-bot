# mastodon-markov-bot
[![Build Status](https://cloud.drone.io/api/badges/mi-24v/mastodon-markov-bot/status.svg?ref=refs/heads/main)](https://cloud.drone.io/mi-24v/mastodon-markov-bot)
## 何これ
Mastodon/Misskey上のアカウントの投稿を、マルコフ連鎖して投稿するBotアプリケーション

デフォルト設定では「非公開」・「DM」は学習せず、投稿を「公開」設定で投稿します(`src/config.yaml`で変更可能です)。 
利用する際は各サーバーのBotガイドラインに従ってください。


例: https://ap.ketsuben.red/@mecha_naf/105073696514947785

## 必要なもの
Dockerが入ったマシン(入れ方は各自調べてください)

## 動かし方 
1. Mastodon/Misskeyのアクセストークンを取得(Mastdonは https://example.com/settings/applications/new から取得可能)
2. `src/sample.env` を `src/.env` にコピー
3. `src/.env` の必要項目を入力(コメントに従って書いてください。)
4. docker-compose up -d でDockerコンテナがビルドされ起動します。

## AWS Lambdaでのデプロイ

aws-sam-cliを用意しておいてください。

```sh
sam build
sam deploy --guided
```
