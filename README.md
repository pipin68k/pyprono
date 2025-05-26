# PyProno 🎤
**英語発音練習プログラム - English Pronunciation Practice Tool**

PyPronoは音声認識技術を活用した英語発音練習プログラムです。システムが英文を読み上げ、あなたの発音を聞き取って評価し、発音スキルの向上をサポートします。

## 🌟 特徴

- **自動音声認識**: Google Speech Recognition APIを使用した高精度な音声認識
- **発音評価システム**: 文字レベルと単語レベルの類似度を組み合わせた総合的な評価
- **Text-to-Speech機能**: システムによるお手本音声の再生
- **カスタムテキスト対応**: 独自のテキストファイルを使用した練習が可能

## 📋 必要要件

### システム要件
- Python 3.6以上
- マイクロフォン
- インターネット接続（音声認識のため）
- Windows 環境

## 🚀 インストール & セットアップ

1. **リポジトリのクローン**
   ```ps
   git clone https://github.com/pipin68k/pyprono.git
   cd pyprono
   ```

2. **必要なライブラリのインストール**
   ```ps
   pip install -r ./requirements.txt
   ```

3. **プログラムの実行**
   ```ps
   python pyprono.py
   ```

## 📂 使用方法

### 基本的な使い方

1. **初回実行時**
   - プログラムを実行すると、`~/Documents/VoiceTutor`フォルダが自動作成されます
   - サンプル練習ファイル（`sample_practice.txt`）も自動生成されます

2. **練習ファイルの準備**
   - `~/Documents/VoiceTutor`フォルダに英文テキストファイル（.txt）を配置
   - 複数のファイルを配置することで、さまざまな内容で練習可能

3. **練習の流れ**
   - システムが英文を読み上げ
   - 同じように発音
   - 音声認識により発音の一致度を評価
   - 目標スコア達成まで最大5回挑戦可能

### サンプルテキストファイル例

```
Hello, I'm Taro.
Nice to meet you.
How are you today?
Thank you very much.
The weather is beautiful.
Have a great day!
```

## ⚙️ 設定

### 音声設定
- 読み上げ速度: 150 WPM（デフォルト）
- 音量: 90%
- 言語: 英語（自動検出）

### 評価基準
- **短文（3語以下）**: 85%以上の一致度が目標
- **長文（4語以上）**: 75%以上の一致度が目標
- 最大試行回数: 5回
