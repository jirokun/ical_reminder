# カレンダーリマインダー

macOSのカレンダーからイベントを取得し、イベント開始時に全画面リマインダーを表示するPythonアプリケーションです。

## 機能

- icalBuddyを使用してmacOSのカレンダーからイベントを定期的に取得
- イベント開始時に全画面リマインダーを表示
- リマインダーは「閉じる」ボタンまたはESCキーで閉じることができる
- 1分後に自動的にリマインダーを閉じる

## 必要条件

- macOS
- Python 3.6以上
- icalBuddy（`brew install ical-buddy`でインストール可能）
- Tkinter（ほとんどのPythonインストールに含まれています）

## インストール

1. リポジトリをクローンまたはダウンロードします
2. icalBuddyがインストールされていない場合は、以下のコマンドでインストールします：
   ```bash
   brew install ical-buddy
   ```

## 使用方法

1. 以下のコマンドでスクリプトを実行します：
   ```bash
   python cal.py
   ```

2. スクリプトはバックグラウンドで実行され、今日のカレンダーイベントをチェックします。

3. イベント開始時に全画面のリマインダーが表示されます。

4. スクリプトを終了するには、ターミナルで `Ctrl+C` を押します。

## ファイル構成

- `cal.py`: メインスクリプト、カレンダーイベントを監視
- `reminder_window.py`: リマインダーのUI表示を担当する独立したスクリプト
- `test_cal.py`: `get_calendar_events` 関数のユニットテスト

## テスト

テストを実行するには：

```bash
# 開発環境の準備
uv venv
source .venv/bin/activate
uv pip install pytest pytest-mock

# テストの実行
python -m pytest
```

## ライセンス

MITライセンス

## 開発メモ

このアプリケーションはmacOSのicalBuddyに依存しています。他のOSで実行するには、適切なカレンダーAPIに置き換える必要があります。
