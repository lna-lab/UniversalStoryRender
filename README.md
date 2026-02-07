# UniversalStoryRender

**Recompose any story into an original world via contextual abstraction.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📖 概要 (Overview)

**UniversalStoryRender** は、既存の物語（小説、脚本など）から「本質的な構造（The Soul）」のみを抽出し、ターゲットとなるドメイン（時代劇、学園青春、SFなど）に合わせて再構成（Rendering）するAIエンジンです。

「忘却（Contextual Forgetting）」を創造の起点とし、原作の固有名詞や時代設定といった「表層（The Skin）」を意図的に破棄することで、著作権や文化的コンテキストの制約を超えた、普遍的な物語の再利用を実現します。

### Key Features

1.  **Contextual Forgetting (文脈的忘却)**
    - ターゲットドメインにそぐわない原作の要素（ノイズ）を能動的に検出し、破棄します。
    - 例: 時代劇版を作る際、原作の「十字架」や「シラクス」といった設定は自動的に忘却されます。

2.  **LNA-ES Ontology (Logically Normalized Architecture for Emotional Structures)**
    - 物語を概念グラフ（ノードとエッジ）として正規化します。
    - 感情曲線（Emotional Arc）を定量化し、異なる世界観でも感動の構造を維持します。

3.  **Domain Adaptation (ドメイン適応)**
    - 抽出された構造に対し、指定されたドメインの語彙やスタイル（Style Formula）を適用して物語を生成します。

## 🚀 デモ実行 (Usage)

本リポジトリには、『走れメロス』を題材としたデモスクリプトが含まれています。

### 前提条件

- Python 3.8+

### セットアップ

```bash
git clone https://github.com/lna-lab/UniversalStoryRender.git
cd UniversalStoryRender
```

### 実行方法

**1. 時代劇版の生成**

```bash
python3 src/main.py --input data/hashire_merosu.md --domain jidai
```

**2. 学園青春版の生成**

```bash
python3 src/main.py --input data/hashire_merosu.md --domain gakuen
```

## 📂 ディレクトリ構成

- `src/`: ソースコード
  - `main.py`: メイン処理スクリプト（構造抽出→忘却→生成）
- `ontology/`: LNA-ES オントロジー定義 (CSV)
  - `foundation/`: 感情定義など
  - `structural/`: 物語構造定義など
  - `cultural/`: ドメインスタイル定義など
- `data/`: サンプルデータ
  - `hashire_merosu.md`: ルビを除去した正規化済みテキスト
- `docs/`: ドキュメント
  - `winning_plan.md`: プロジェクトの全体構想・優勝プラン
  - `presentation_script.md`: プレゼンテーション原稿

## 📜 ライセンス

MIT License

Copyright (c) 2026 lna-lab inc.
