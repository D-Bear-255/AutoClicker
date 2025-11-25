import customtkinter as ctk       # UI用
import pyautogui           # クリック、キー入力自動化用
import time                # 待ち時間制御用
import threading            # UIを止めずに別の動作を同時進行させる用
from pynput import keyboard # キー入力監視用
import winsound # エラー音鳴らす用

# ホットキーで連打開始を作るのと、エラーダイアログ出す機能も付けてもいいかも

# 押したかテスト用ボタン
def test():
    print("testボタンが押されました")

# ホットキー監視用
current_key = None

def on_press(key):
    global current_key
    current_key = key
    print("☆キー監視発動 入力キー=" + str(current_key))

    # 特殊キーは str で取る
    try:
        name = key.char.lower()
    except:
        name = str(key).replace("Key.", "").lower()

    if name == start_hotkey.get():   # 連打開始キー
        start_clicking()

    elif name == stop_hotkey.get():  # 連打停止キー
        stop_clicking()


listener = keyboard.Listener(on_press=on_press)
listener.daemon = True
listener.start()

# クリックを続けるフラグ
running = False

# 連打開始
def start_clicking():
    global running
    # 連打は1スレッドのみ扱う
    if not running:
        print("☆連打開始 click_mode=" + str(click_mode.get()))
        error = False
        running = True
        click_time = interval.get()
        # ラベルのテキストを変更
        status_label.configure(text="連打中", text_color="lime")
        # クリック対象に合わせて処理を変更
        # 左クリック
        if click_mode.get() == "left":
            def click_loop():
                while running:
                    time.sleep(click_time)  # 入力した秒数だけ待つ
                    pyautogui.click()           # 左クリック

            
        # 右クリック
        elif click_mode.get() == "right":
            def click_loop():
                while running:
                    time.sleep(click_time)  # 入力した秒数だけ待つ
                    pyautogui.rightClick()           # 右クリック


        # キーボード入力
        elif click_mode.get() == "keyboard":
            press_key = input_key.get()
            if is_valid_key(press_key):
                print("☆入力処理対応キーです input_key=" + str(press_key))
                def click_loop():
                    while running:
                        time.sleep(click_time)  # 入力した秒数だけ待つ
                        pyautogui.press(press_key)           # キーボード入力

            else:
                print("☆入力処理非対応対応キーです input_key=" + str(press_key))
                error = True
        
        # エラーでなければスレッドでループ開始
        if not error:
            threading.Thread(target=click_loop, daemon=True).start()
        # エラーの場合はクリック停止処理を実施
        else:
            stop_clicking()
        
    
    # すでに連打開始済みの場合は何もしない
    else:
        print("☆連打開始済")
    
# 連打終了
def stop_clicking():
    global running
    if running:
        running = False
        # ラベルのテキストを変更
        status_label.configure(text="待機中", text_color="white")
        print("☆連打終了")
    else:
        print("☆連打終了済")
        winsound.MessageBeep()

# キーボード入力部分表示
def update_key_entry():
    # キーボード入力をラジオボタンで指定されていた時に表示
    if click_mode.get() == "keyboard":
        key_label.grid(row=4, column=0, pady=5, padx=5, sticky="w")
        key_entry.grid(row=5, column=0, pady=5, padx=5, sticky="w")
    else:
        key_label.grid_forget()
        key_entry.grid_forget()

# キーボード入力処理の対応文字かのチェック
def is_valid_key(key: str) -> bool:
    return key.lower() in pyautogui.KEYBOARD_KEYS

# --- UI部分 ---
# テーマ設定
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue") 

# メインウィンドウ作成
root = ctk.CTk()
root.title("連ツくん")
root.geometry("400x300")

# 左フレーム
left_frame = ctk.CTkFrame(root)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

# 右フレーム
right_frame = ctk.CTkFrame(root)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# 左側要素
# 連打状態表示
status_label = ctk.CTkLabel(left_frame, text="待機中")
status_label.grid(row=0, column=0, pady=5)

# 入力欄用フレーム
etr_frame = ctk.CTkFrame(left_frame)
etr_frame.grid(row=1, column=0, pady=5, padx=5)

# 間隔の入力欄
interval = ctk.DoubleVar(value=2)
interval_label = ctk.CTkLabel(etr_frame, text="クリック間隔（秒）")
interval_entry = ctk.CTkEntry(etr_frame, textvariable=interval, width=140)

interval_label.grid(row=1, column=0, pady=5)
interval_entry.grid(row=2, column=0, padx=2)

# ホットキー指定用フレーム
hotkey_frame = ctk.CTkFrame(left_frame)
hotkey_frame.grid(row=2, column=0, pady=5, padx=5)

# ホットキー入力欄
start_hotkey = ctk.StringVar(value="f8")
stop_hotkey = ctk.StringVar(value="f9")
start_hotkey_label = ctk.CTkLabel(hotkey_frame, text="連打開始ホットキー")
start_hotkey_entry = ctk.CTkEntry(hotkey_frame, textvariable=start_hotkey, width=140)
stop_hotkey_label = ctk.CTkLabel(hotkey_frame, text="連打終了ホットキー")
stop_hotkey_entry = ctk.CTkEntry(hotkey_frame, textvariable=stop_hotkey, width=140)

start_hotkey_label.grid(row=1, column=0, pady=5)
start_hotkey_entry.grid(row=2, column=0, padx=2)
stop_hotkey_label.grid(row=3, column=0, pady=5)
stop_hotkey_entry.grid(row=4, column=0, padx=2)

# 右側要素
right_frame.columnconfigure(0, weight=0)
right_frame.columnconfigure(1, weight=0)

# ボタン用フレーム
btn_frame = ctk.CTkFrame(right_frame)
btn_frame.grid(row=0, column=0, pady=5, padx=5, sticky="w")

# 開始・停止ボタン
start_btn = ctk.CTkButton(btn_frame, text="開始", command=start_clicking, width=90)
stop_btn  = ctk.CTkButton(btn_frame, text="停止", command=stop_clicking, width=90)
test_btn = ctk.CTkButton(right_frame, text="test", command=test , width=190)

start_btn.grid(row=0, column=0, padx=(0,5), pady=5, sticky="w")
stop_btn.grid(row=0, column=1, padx=(5,0), pady=5, sticky="w")
#これはテスト用ボタン 常に一番下のrowに入れておく
#test_btn.grid(row=2, column=0, pady=5, sticky="w", columnspan=2)

# モード用フレーム
mode_frame = ctk.CTkFrame(right_frame)
mode_frame.grid(row=1, column=0, pady=5, padx=5, sticky="w")

# モード選択
mode_label = ctk.CTkLabel(mode_frame, text="・連打対象")
mode_label.grid(row=0, column=0, pady=5, padx=5, sticky="w")

click_mode = ctk.StringVar(value="left")  # 初期値は左クリック
radio_left  = ctk.CTkRadioButton(mode_frame, text="左クリック", variable=click_mode, command=update_key_entry, value="left")
radio_right = ctk.CTkRadioButton(mode_frame, text="右クリック", variable=click_mode, command=update_key_entry, value="right")
radio_key   = ctk.CTkRadioButton(mode_frame, text="キーボード入力", variable=click_mode, command=update_key_entry, value="keyboard")

radio_left.grid(row=1, column=0, pady=5, padx=5, sticky="w")
radio_right.grid(row=2, column=0, pady=5, padx=5, sticky="w")
radio_key.grid(row=3, column=0, pady=5, padx=5, sticky="w")

#キーボード入力指定時に出るやつ
input_key = ctk.StringVar(value="A")
key_label = ctk.CTkLabel(mode_frame, text="・対象キー")
key_entry = ctk.CTkEntry(mode_frame, textvariable=input_key, width=70)

root.mainloop()