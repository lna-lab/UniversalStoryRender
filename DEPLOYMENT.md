# デプロイメントガイド (Deployment Guide)

このプロジェクトは、**Render.com** などのPaaS（Platform as a Service）に簡単にデプロイできるように構成されています。
フロントエンド（HTML/JS）とバックエンド（FastAPI/Python）が一体となっているため、1つのWebサービスとしてデプロイするだけで、`http://lna-lab.com/` のような独自ドメインで公開可能な「自己完結型プロダクト」として動作します。

## 推奨プラットフォーム: Render.com

### 手順 1: Render.com アカウント作成
1. [Render.com](https://render.com/) にアクセスし、GitHubアカウントでサインアップします。

### 手順 2: 新規Webサービスの作成
1. ダッシュボードの "New +" ボタンから **"Web Service"** を選択します。
2. "Connect a repository" で `lna-lab/UniversalStoryRender` を選択します。

### 手順 3: 設定入力
以下の設定を入力します（多くは自動検出されます）。

- **Name**: `universal-story-renderer` (任意)
- **Region**: 最寄りのリージョン (例: Singapore, Oregon)
- **Branch**: `main`
- **Root Directory**: `.` (空欄でOK)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
- **Instance Type**: `Free` (ハッカソン用途なら十分です)

### 手順 4: 環境変数の設定 (重要)
"Environment Variables" セクションまでスクロールし、APIキーを設定します。

- **Key**: `GLM_API_KEY`
- **Value**: (あなたのZhipuAI APIキー)

"Create Web Service" をクリックしてデプロイを開始します。

### 手順 5: 動作確認
数分でデプロイが完了します。画面左上のURL（例: `https://universal-story-renderer.onrender.com`）にアクセスし、アプリが動くことを確認してください。

---

## 独自ドメイン (lna-lab.com) の設定

作成したサービスを `http://lna-lab.com/` で公開するための設定です。

1. Renderのダッシュボードで、デプロイしたサービスの **"Settings"** タブを開きます。
2. **"Custom Domains"** セクションを見つけ、"Add Custom Domain" をクリックします。
3. ドメイン名 `lna-lab.com` を入力します。
4. 画面に表示される指示に従って、ドメイン管理画面（お名前.com、GoDaddyなど）でDNSレコードを設定します。
    - **Type**: `CNAME` (または `A` レコード。Renderの指示に従ってください)
    - **Name**: `@` (または `www`)
    - **Value**: `universal-story-renderer.onrender.com` (あなたのRenderアプリのURL)
5. DNSの反映を待ちます（数分〜数時間）。反映されると、`http://lna-lab.com/` でアプリが利用可能になります。Renderが自動的にSSL証明書を発行するため、`https://` も利用可能になります。
