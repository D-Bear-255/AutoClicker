# 連打ツール (AutoClicker)
シンプルなGUIベースの連打ツールです。<br>
左クリック、右クリック、指定キー入力の連打に対応し、ホットキーによる開始・停止にも対応しています。

## できること
・右クリック、左クリック、任意のキーボードの連打<br>
・連打間隔を数値で指定<br>
・ホットキーでの連打開始、停止<br>
・連打開始、停止するホットキーの指定<br>

## スクリーンショット
<img width="502" height="414" alt="image" src="https://github.com/user-attachments/assets/07ef552a-a022-4229-891b-e7f1f03dcb67" />

## 操作方法
1.連打対象をラジオボタンで選択<br>
2.連打間隔を指定する(デフォルトでは2秒)<br>
3.開始ボタンもしくは連打開始ホットキーを押して連打開始<br>
4.停止ボタンもしくは連打終了ホットキーを押して連打終了

## 開発環境
・Python 3.13.7<br>
・customtkinter<br>
・pyautogui<br>
・time<br>
・threading<br>
・pynput<br>
・winsound

## 実行ファイルの作成方法（メモ）
PyInstaller を使用する<br>
> pyinstaller --onefile --windowed --name AutoClicker 連ツ.py
