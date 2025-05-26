#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pyprono - 英語発音練習プログラム

必要なライブラリのインストール:
pip install pyttsx3 speech_recognition pyaudio difflib

Windowsの場合、追加で以下も必要:
pip install pywin32
"""

import os
import glob
import pyttsx3
import speech_recognition as sr
import pyaudio
import difflib
import re
import time
from pathlib import Path

class VoiceTutor:
    def __init__(self):
        # Text-to-Speech エンジンの初期化
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Speech Recognition の初期化
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # マイクの調整
        self.adjust_microphone()

        print("🎤 VoiceTutor - 英語発音練習プログラム 🎤")
        print("=" * 60)
    
    def setup_tts(self):
        """Text-to-Speech エンジンの設定"""
        # 音声の設定
        voices = self.tts_engine.getProperty('voices')
        
        # 英語音声を探す
        english_voice = None
        for voice in voices:
            if 'english' in voice.name.lower() or 'en-' in voice.id.lower():
                english_voice = voice
                break
        
        if english_voice:
            self.tts_engine.setProperty('voice', english_voice.id)
            print(f"音声エンジン: {english_voice.name}")
        else:
            print("英語音声が見つかりませんでした。デフォルト音声を使用します。")
        
        # 速度とボリュームの設定
        self.tts_engine.setProperty('rate', 150)  # 少し遅めに設定
        self.tts_engine.setProperty('volume', 0.9)
    
    def adjust_microphone(self):
        """マイクロフォンの環境雑音レベルを調整"""
        print("マイクロフォンの環境音を調整中...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("調整完了！")
    
    def read_text_files(self, folder_path="Documents/VoiceTutor"):
        """指定フォルダ内のテキストファイルを読み込む"""
        # Documentsフォルダのパスを取得
        if folder_path == "Documents/VoiceTutor":
            documents_path = Path.home() / "Documents" / "VoiceTutor"
        else:
            documents_path = Path(folder_path)
        
        # フォルダが存在しない場合は作成
        if not documents_path.exists():
            try:
                documents_path.mkdir(parents=True, exist_ok=True)
                print(f"📁 練習用フォルダを作成しました: {documents_path}")
                print("📝 このフォルダに英文テキストファイル(.txt)を配置してください。")
                
                # サンプルファイルを作成
                sample_file = documents_path / "sample_practice.txt"
                sample_content = """Hello, I'm Taro.
Nice to meet you.
How are you today?
Thank you very much.
The weather is beautiful.
Have a great day!
"""
                with open(sample_file, 'w', encoding='utf-8') as f:
                    f.write(sample_content)
                print(f"📄 サンプル練習ファイルを作成しました: {sample_file.name}")
                
            except Exception as e:
                print(f"フォルダ作成エラー: {e}")
                return []
        
        # テキストファイルを検索
        text_files = []
        patterns = ['*.txt', '*.text']
        
        for pattern in patterns:
            text_files.extend(documents_path.glob(pattern))
        
        if not text_files:
            print(f"'{documents_path}' にテキストファイルが見つかりませんでした。")
            if documents_path.name == "VoiceTutor":
                print("💡 ヒント: サンプルファイルが作成されているので、それを使って練習できます！")
            return []
        
        # ファイル内容を読み込み
        texts = []
        for file_path in text_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        texts.append({
                            'file': file_path.name,
                            'content': content
                        })
                        print(f"読み込み完了: {file_path.name}")
            except Exception as e:
                print(f"ファイル読み込みエラー: {file_path.name} - {e}")
        
        return texts
    
    def extract_sentences(self, text):
        """テキストから文章を抽出する"""
        # 改行でも分割して、短い文章も含める
        lines = text.split('\n')
        sentences = []
        
        for line in lines:
            line = line.strip()
            if line:
                # 文章の区切り文字で分割
                line_sentences = re.split(r'[.!?]+', line)
                sentences.extend(line_sentences)
        
        # 空の文章を除外（短い文章も含める）
        valid_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            # 最低3文字以上で、英数字を含む文章を有効とする
            if len(sentence) >= 3 and any(c.isalnum() for c in sentence):
                valid_sentences.append(sentence)
        
        return valid_sentences
    
    def speak_text(self, text):
        """テキストを音声で読み上げる"""
        print(f"システム音声: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen_user_speech(self, timeout=10):
        """ユーザーの音声を認識する"""
        try:
            print("あなたの発音を聞いています... （話し始めてください）")
            with self.microphone as source:
                # タイムアウト付きで音声を録音
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            print("音声を認識中...")
            # Google Speech Recognition を使用
            user_text = self.recognizer.recognize_google(audio, language='en-US')
            return user_text.lower().strip()
            
        except sr.WaitTimeoutError:
            print("タイムアウトしました。もう一度お試しください。")
            return None
        except sr.UnknownValueError:
            print("音声を認識できませんでした。もう一度お試しください。")
            return None
        except sr.RequestError as e:
            print(f"音声認識サービスエラー: {e}")
            return None
    
    def calculate_similarity(self, original, spoken):
        """発音の類似度を計算する"""
        # 文字列の前処理（句読点や大文字小文字を統一）
        original_clean = re.sub(r'[^\w\s]', '', original.lower().strip())
        spoken_clean = re.sub(r'[^\w\s]', '', spoken.lower().strip())
        
        # 単語レベルでの比較も追加
        original_words = original_clean.split()
        spoken_words = spoken_clean.split()
        
        # 文字列全体の類似度
        char_similarity = difflib.SequenceMatcher(None, original_clean, spoken_clean).ratio()
        
        # 単語レベルの類似度
        word_similarity = difflib.SequenceMatcher(None, original_words, spoken_words).ratio()
        
        # 両方の類似度を重み付けして計算（単語レベルを重視）
        final_similarity = (char_similarity * 0.3 + word_similarity * 0.7) * 100
        
        return final_similarity
    
    def practice_sentence(self, sentence):
        """1つの文章で発音練習する"""
        print("\n" + "=" * 60)
        print(f"練習文: {sentence}")
        print("=" * 60)
        
        max_attempts = 5
        # 短い文章は少し厳しめ、長い文章は少し緩めに設定
        if len(sentence.split()) <= 3:  # 3語以下の短い文章
            target_similarity = 85  
        else:
            target_similarity = 75  # 長い文章は少し緩め
        
        for attempt in range(1, max_attempts + 1):
            print(f"\n--- 試行 {attempt}/{max_attempts} ---")
            
            # システムが文章を読み上げ
            print("1. システムの発音を聞いてください:")
            self.speak_text(sentence)
            
            # ユーザーに発音を促す
            print("2. 同じように発音してください:")
            user_speech = self.listen_user_speech()
            
            if user_speech is None:
                continue
            
            print(f"認識された音声: {user_speech}")
            
            # 類似度を計算
            similarity = self.calculate_similarity(sentence, user_speech)
            print(f"発音の一致度: {similarity:.1f}%")
            
            if similarity >= target_similarity:
                print("🎉 素晴らしい発音です！")
                return True
            else:
                print(f"もう少しです。目標: {target_similarity}%以上")
                if attempt < max_attempts:
                    print("もう一度挑戦してください。")
                    time.sleep(1)
        
        print(f"⏰ {max_attempts}回の試行が終了しました。次の文章に進みます。")
        return False
    
    def run(self):
        """メインプログラムを実行"""
        # テキストファイルを読み込み
        texts = self.read_text_files()
        
        if not texts:
            print("練習用のテキストファイルを ~/Documents/VoiceTutor フォルダに配置してください。")
            print("📁 フォルダが存在しない場合は自動作成され、サンプルファイルも用意されます。")
            print("📄 ファイル例: practice.txt, daily_conversation.txt など")
            return
        
        print(f"\n{len(texts)} 個のファイルが見つかりました。")
        
        # 各ファイルを処理
        for text_data in texts:
            print(f"\n📄 ファイル: {text_data['file']}")
            sentences = self.extract_sentences(text_data['content'])
            
            if not sentences:
                print("有効な文章が見つかりませんでした。")
                continue
            
            print(f"📝 {len(sentences)} 個の文章で練習します。")
            
            # 各文章で練習
            for i, sentence in enumerate(sentences, 1):
                print(f"\n🎯 文章 {i}/{len(sentences)}")
                
                # ユーザーに継続確認
                if i > 1:
                    continue_practice = input("\n次の文章に進みますか？ (y/n/q=終了): ").lower()
                    if continue_practice == 'q':
                        print("練習を終了します。")
                        return
                    elif continue_practice == 'n':
                        continue
                
                # 文章で練習
                self.practice_sentence(sentence)
        
        print("\n🎊 Congratulations! 全ての発音レッスンが完了しました！")
        print("Keep practicing and you'll become even better!")

def main():
    """メイン関数"""
    try:
        checker = VoiceTutor()
        checker.run()
    except KeyboardInterrupt:
        print("\n\nプログラムを終了します。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("必要なライブラリがインストールされているか確認してください。")

if __name__ == "__main__":
    main()
