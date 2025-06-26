# Math Word Problem Generator

日本の学習指導要領に準拠した数学文章問題生成ツール

## 概要

**Math Word Problem Generator**は、学年（1-12年）と難易度（1-5）を指定することで、日本のカリキュラムに合った数学の文章問題を自動生成するWebアプリケーションです。

### 主な機能

- **学年別カリキュラム対応**: 小学1年生から高校3年生まで、各学年の学習内容に応じた問題を生成
- **難易度調整**: 5段階の難易度設定で、数値の大きさや問題の複雑さを調整
- **7段階ヒント機能**: 軽いヒントから完全解答まで、段階的にヒントを表示
- **印刷対応**: A4用紙1枚に収まるよう最適化された印刷レイアウト
- **レスポンシブデザイン**: デスクトップからモバイルまで対応

### 問題数

- **小学生（1-6年）**: 5問
- **中学生（7-9年）**: 3問  
- **高校生（10-12年）**: 1問

## 技術スタック

### バックエンド
- **FastAPI**: Pythonの高速Webフレームワーク
- **Pydantic**: データバリデーション
- **Uvicorn**: ASGIサーバー

### フロントエンド
- **HTML5/CSS3**: セマンティックマークアップ
- **JavaScript (ES6+)**: フロントエンド機能
- **Responsive Design**: モバイル対応

## セットアップ

### 必要な環境

- Python 3.8以上
- pip (Python package manager)

### インストール手順

1. **リポジトリのクローンまたはダウンロード**

```bash
git clone <repository_url>
cd math-word-problem-generator
```

2. **仮想環境の作成と有効化**

```bash
# 仮想環境作成
python -m venv .venv

# 仮想環境有効化 (macOS/Linux)
source .venv/bin/activate

# 仮想環境有効化 (Windows)
.venv\Scripts\activate
```

3. **依存関係のインストール**

```bash
pip install -r backend/requirements.txt
```

4. **バックエンドサーバーの起動**

```bash
# 仮想環境を有効化してから起動
source .venv/bin/activate  # macOS/Linux
# または .venv\Scripts\activate  # Windows

uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

5. **フロントエンドの起動**

シンプルなHTTPサーバーでフロントエンドを起動します：

```bash
# Python 3の場合
python -m http.server 5500 --directory frontend

# または、任意のHTTPサーバーを使用
# 例: Live Server (VS Code拡張)、Apache、Nginxなど
```

6. **アクセス**

- **フロントエンド**: http://localhost:5500
- **API仕様**: http://localhost:8000/docs

## 使い方

### Webインターフェース

1. ブラウザで http://localhost:5500 にアクセス
2. 学年を選択（小学1年生〜高校3年生）
3. 難易度を選択（1: 易しい 〜 5: 難しい）
4. 「問題を生成」ボタンをクリック
5. 生成された問題を確認
6. 「ヒントを表示」で段階的ヒントを確認
7. **ヒント6・7で具体的な式と答えを確認**
8. 「印刷」ボタンでA4用紙に印刷

### API直接利用

```bash
# 小学3年生、難易度2の問題を生成
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"grade": 3, "difficulty": 2}'
```

## プロジェクト構造

```
math-word-problem-generator/
├── .venv/                      # 仮想環境（新規作成後）
├── backend/                    # バックエンド（FastAPI）
│   ├── __init__.py
│   ├── app.py                 # FastAPIアプリケーション
│   ├── generator.py           # 問題・ヒント生成ロジック
│   ├── curriculum_map.py      # カリキュラムマッピング
│   └── requirements.txt       # Python依存関係
├── frontend/                   # フロントエンド
│   ├── index.html            # メインHTML
│   ├── css/
│   │   └── style.css         # スタイルシート
│   └── js/
│       └── main.js           # JavaScript機能
├── tests/                      # テスト
│   └── test_generator.py     # ユニットテスト
├── README.md                   # このファイル
└── .gitignore                 # Git除外設定
```

## ヒント機能の詳細

### 7段階ヒントシステム

1. **ヒント1-2**: 軽いヒント（問題のタイプ、キーワード）
2. **ヒント3-5**: 核心的ヒント（解法の方向性、計算方法）
3. **ヒント6**: 具体的な計算式（例: `式: 6 + 7 = 13`）
4. **ヒント7**: 完全な答え（例: `答え: 13個`）

### 対応している問題タイプ

- **四則演算**: たし算、ひき算、かけ算、わり算
- **図形**: 面積、体積の計算
- **単位**: 個、g、cm、mL、円、㎠、㎤など

## テスト

```bash
# 仮想環境を有効化
source .venv/bin/activate

# 全テスト実行
python -m pytest tests/ -v

# 特定のテストクラス実行
python -m pytest tests/test_generator.py::TestGenerateProblems -v
```

## トラブルシューティング

### よくある問題

#### 1. 仮想環境が有効化されていない

**症状**: モジュールが見つからないエラー

**解決方法**:
```bash
# 仮想環境を有効化
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# 確認
which python  # 仮想環境のパスが表示されること
```

#### 2. バックエンドが起動しない

**解決方法**:
```bash
# 仮想環境で依存関係を再インストール
source .venv/bin/activate
pip install -r backend/requirements.txt

# サーバー起動
uvicorn backend.app:app --reload
```

#### 3. ヒント機能で式が表示されない

**症状**: ヒント6・7で「計算式を立てましょう」などの汎用メッセージ

**原因と解決方法**:
- 問題のタイプが正しく識別されていない可能性
- 数値が正しく抽出されていない可能性
- 問題文に「合わせて」「残り」などのキーワードが含まれているか確認

## 開発環境での注意事項

### 仮想環境の使用

本プロジェクトでは**必ず仮想環境**を使用してください：

```bash
# 仮想環境作成（初回のみ）
python -m venv .venv

# 毎回の作業開始時に有効化
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# 作業終了時に非有効化
deactivate
```

### 依存関係の管理

新しいパッケージを追加した場合：

```bash
# 仮想環境で追加
pip install <package_name>

# requirements.txtを更新
pip freeze > backend/requirements.txt
```

## 更新履歴

### v1.1.0 (現在)
- 🔥 **仮想環境対応**: .venvを使用した環境分離
- ⚡ **ヒント改善**: 7段階目で具体的な式と答えを表示
- 🎯 **問題タイプ識別向上**: より正確な計算結果

### v1.0.0 (初回リリース)
- 基本的な問題生成機能
- 7段階ヒントシステム
- レスポンシブデザイン
- 印刷対応機能

---

## サポート

質問や問題がある場合は、GitHubのIssuesページで報告してください。

**Happy Learning! 📚✨**