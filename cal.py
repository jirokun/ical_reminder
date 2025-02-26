#!/usr/bin/env python3
"""
カレンダーリマインダースクリプト

icalBuddyを使用してカレンダーイベントを取得し、イベントの開始時刻に全画面リマインダーを表示します。

必要条件:
- icalBuddyがインストールされているmacOS (brew install ical-buddy)
- Python 3.6+
- Tkinter (ほとんどのPythonインストールに含まれています)

使用方法:
    python calendar_reminder.py
"""

import subprocess
import time
import datetime
import re
import os
import sys
import subprocess

def get_calendar_events():
    """
    icalBuddyを使用してカレンダーイベントを取得します。
    
    戻り値:
        list: (event_time, event_title)のタプルを含むリスト
    """
    # icalBuddyを実行して今日のイベントを取得
    cmd = ["icalBuddy", "eventsToday"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"icalBuddyの実行エラー: {result.stderr}")
            return []
        
        output = result.stdout.strip()
        if not output:
            return []
        
        events = []
        lines = output.split('\n')
        
        current_title = None
        
        for line in lines:
            line = line.strip()
            
            # 行頭の「•」を含む行がイベントタイトル
            if line.startswith('•'):
                current_title = line[1:].strip()
                continue
                
            # インデントされた行には時間情報がある
            # 例: "10:00 - 14:00"
            time_pattern = r'(\d{1,2}:\d{2})\s*-\s*\d{1,2}:\d{2}'
            match = re.search(time_pattern, line)
            
            if match and current_title:
                start_time_str = match.group(1)  # 開始時間
                title = current_title           # 前の行で読み取ったタイトル
                
                try:
                    # 時間文字列を解析
                    today = datetime.datetime.now().date()
                    hours, minutes = map(int, start_time_str.split(':'))
                    
                    event_time = datetime.datetime.combine(today, datetime.time(hours, minutes))
                    
                    # 過去のイベントで、最後の1時間以内でなければ無視
                    current_time = datetime.datetime.now()
                    if event_time < current_time and (current_time - event_time).total_seconds() > 3600:
                        continue
                    
                    print(f"イベントを解析: {start_time_str} - {title}")
                    events.append((event_time, title))
                except ValueError as e:
                    print(f"時間解析エラー: {line} - {e}")
            elif line and not any(c.isdigit() for c in line):
                # 時間が設定されていないイベント（終日イベント）
                # 例: "ダンス衣装持っていく"
                # このコードをコメント解除すると終日イベントに対して朝9時にリマインダーを表示
                
                # title = line.strip()
                # today = datetime.datetime.now().date()
                # # 終日イベントは朝9時にリマインダー
                # event_time = datetime.datetime.combine(today, datetime.time(9, 0))
                # 
                # # 過去のイベントは無視
                # current_time = datetime.datetime.now()
                # if event_time < current_time:
                #     continue
                # 
                # print(f"終日イベントを解析: {title}")
                # events.append((event_time, f"[終日] {title}"))
                pass
        
        return events
    except Exception as e:
        print(f"エラー: {e}")
        return []

def display_fullscreen_reminder(event_title):
    """
    イベントの全画面リマインダーを表示します。
    
    引数:
        event_title (str): イベントのタイトル
    """
    
    # 外部スクリプトのパス
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reminder_window.py")
    
    # スクリプトの存在確認
    if not os.path.exists(script_path):
        print(f"エラー: リマインダースクリプトが見つかりません: {script_path}")
        return
    
    try:
        # イベントタイトルをコマンドライン引数として渡す
        cmd = [sys.executable, script_path, event_title]
        
        # 新しいプロセスでスクリプトを実行（標準出力と標準エラー出力を捨てる）
        # ウィンドウが独立したプロセスで動作するようにする
        subprocess.run(cmd, check=True, 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("リマインダーウィンドウが異常終了しました")
    except KeyboardInterrupt:
        print("キーボード割り込みによりリマインダーを終了しました")

def main():
    """イベントを継続的にチェックするメイン関数。"""
    print("カレンダーリマインダースクリプトを開始しました。")
    print("終了するには Ctrl+C を押してください。")
    
    last_check_time = None
    events = []
    
    while True:
        current_time = datetime.datetime.now()
        
        # 1分ごとにイベントリストを更新
        if last_check_time is None or (current_time - last_check_time).total_seconds() >= 60:
            print(f"{current_time.strftime('%H:%M:%S')} にイベントを更新しています")
            events = get_calendar_events()
            last_check_time = current_time
            
            # 今後のイベントを表示
            if events:
                print("今後のイベント:")
                for event_time, event_title in sorted(events):
                    time_diff = (event_time - current_time).total_seconds()
                    if time_diff > 0:  # 将来のイベントのみ表示
                        print(f"  {event_time.strftime('%H:%M')} - {event_title}")
            else:
                print("今日のイベントは見つかりませんでした。")
        
        # 今後1分以内に開始するイベントがあるかチェック
        for event_time, event_title in list(events):  # 反復のためにリストのコピーを使用
            time_diff = (event_time - current_time).total_seconds()
            
            # イベントが今後1分以内に開始する場合
            if 0 <= time_diff <= 60:
                print(f"{event_time.strftime('%H:%M')}に開始するイベント: {event_title}")
                display_fullscreen_reminder(event_title)
                
                # 複数のリマインダーを表示しないようにリストからこのイベントを削除
                events = [e for e in events if e[0] != event_time or e[1] != event_title]
        
        # 10秒待ってから再度チェック
        time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nカレンダーリマインダースクリプトを停止しました。")