#!/usr/bin/env python3
"""
リマインダーウィンドウを表示するスクリプト

このスクリプトは単体で実行され、フルスクリーンのリマインダーウィンドウを表示します。
"""

import tkinter as tk
from tkinter import font
import time
import sys


def main():
    # コマンドライン引数からイベントタイトルを取得
    if len(sys.argv) > 1:
        event_title = sys.argv[1]
    else:
        event_title = "不明なイベント"

    # Tkルートウィンドウの作成
    root = tk.Tk()
    root.title("カレンダーリマインダー")
    root.attributes('-fullscreen', True)
    
    # フレーム作成
    frame = tk.Frame(root, bg="black")
    frame.pack(fill=tk.BOTH, expand=True)
    
    # フォント作成
    title_font = font.Font(family="Arial", size=36, weight="bold")
    time_font = font.Font(family="Arial", size=24)
    
    # 現在時刻
    time_label = tk.Label(
        frame,
        text=f"現在時刻: {time.strftime('%H:%M')}",
        font=time_font,
        bg="black",
        fg="white"
    )
    time_label.pack(pady=(100, 50))
    
    # イベントタイトル
    title_label = tk.Label(
        frame,
        text=f"イベント開始: {event_title}",
        font=title_font,
        wraplength=root.winfo_screenwidth() - 100,
        justify=tk.CENTER,
        bg="black",
        fg="white"
    )
    title_label.pack(pady=50)
    
    # 閉じるボタン関数
    def close_window():
        root.destroy()
        sys.exit(0)
    
    # ESCキーでも閉じる
    root.bind('<Escape>', lambda e: close_window())
    
    # 閉じるボタン
    close_btn = tk.Button(
        frame,
        text="閉じる",
        font=font.Font(family="Arial", size=24, weight="bold"),
        command=close_window,
        bg="red",
        fg="white",
        padx=30,
        pady=15,
        relief=tk.RAISED,
        borderwidth=5
    )
    close_btn.pack(pady=50)
    close_btn.focus_set()
    
    # 自動終了タイマー
    root.after(60000, close_window)
    
    # ウィンドウを前面に
    root.lift()
    root.attributes("-topmost", True)
    
    # ×ボタンのハンドラ
    root.protocol("WM_DELETE_WINDOW", close_window)
    
    # メインループ開始
    root.mainloop()


if __name__ == "__main__":
    main()