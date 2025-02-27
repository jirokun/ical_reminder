#!/usr/bin/env python3
from unittest.mock import patch, Mock
import datetime
from cal import get_calendar_events


@patch("cal.subprocess.run")
def test_get_calendar_events_success(mock_run: Mock) -> None:
    # Mock subprocess.run to return successful output with actual format
    mock_process = Mock()
    mock_process.returncode = 0
    mock_process.stdout = """• テスト (次郎共有)
    1:00 - 2:00
• バイト (幸恵共有予定)
    10:00 - 14:00
• 鈴木歯科 (幸恵共有予定)
    16:30 - 17:30"""
    mock_run.return_value = mock_process

    # Freeze time at 0:30 AM (early time to ensure all events are in the future)
    with patch("cal.datetime") as mock_datetime:
        mock_datetime.datetime.now.return_value = datetime.datetime(2025, 2, 27, 0, 30)
        mock_datetime.datetime.combine = datetime.datetime.combine
        mock_datetime.time = datetime.time

        events = get_calendar_events()

        # The current regex pattern in cal.py might not match this format
        # If the test fails, we need to update the pattern in cal.py

        # Verify events were parsed correctly
        # Note: This may fail if the actual format isn't matched correctly
        assert len(events) == 3

        # Check events - note time format may need adjustment in cal.py
        assert events[0][0] == datetime.datetime(2025, 2, 27, 1, 0)
        assert "テスト" in events[0][1]

        assert events[1][0] == datetime.datetime(2025, 2, 27, 10, 0)
        assert "バイト" in events[1][1]

        assert events[2][0] == datetime.datetime(2025, 2, 27, 16, 30)
        assert "鈴木歯科" in events[2][1]


@patch("cal.subprocess.run")
def test_get_calendar_events_empty(mock_run: Mock) -> None:
    # Mock subprocess.run to return empty output
    mock_process = Mock()
    mock_process.returncode = 0
    mock_process.stdout = ""
    mock_run.return_value = mock_process

    events = get_calendar_events()

    # Verify no events were returned
    assert events == []


@patch("cal.subprocess.run")
def test_get_calendar_events_error(mock_run: Mock) -> None:
    # Mock subprocess.run to return error
    mock_process = Mock()
    mock_process.returncode = 1
    mock_process.stderr = "Command not found: icalBuddy"
    mock_run.return_value = mock_process

    events = get_calendar_events()

    # Verify no events were returned due to error
    assert events == []


@patch("cal.subprocess.run")
def test_get_calendar_events_past_events(mock_run: Mock) -> None:
    # Mock subprocess.run to return past events
    mock_process = Mock()
    mock_process.returncode = 0
    mock_process.stdout = "• 08:00 - 09:00: 過去のイベント"
    mock_run.return_value = mock_process

    # Freeze time at 10:00 AM
    with patch("cal.datetime") as mock_datetime:
        mock_datetime.datetime.now.return_value = datetime.datetime(2025, 2, 27, 10, 0)
        mock_datetime.datetime.combine = datetime.datetime.combine
        mock_datetime.time = datetime.time

        events = get_calendar_events()

        # Verify past events more than 1 hour ago are filtered out
        assert events == []


@patch("cal.subprocess.run")
def test_get_calendar_events_with_dots_format(mock_run: Mock) -> None:
    # Mock subprocess.run to return event with "..." end time format
    mock_process = Mock()
    mock_process.returncode = 0
    mock_process.stdout = """• test (次郎共有)
    23:09 - ..."""
    mock_run.return_value = mock_process

    # Freeze time at 22:00 (to make sure the event is in the future)
    with patch("cal.datetime") as mock_datetime:
        mock_datetime.datetime.now.return_value = datetime.datetime(2025, 2, 27, 22, 0)
        mock_datetime.datetime.combine = datetime.datetime.combine
        mock_datetime.time = datetime.time

        events = get_calendar_events()

        # Verify event with "..." format was parsed correctly
        assert len(events) == 1
        assert events[0][0] == datetime.datetime(2025, 2, 27, 23, 9)
        assert "test" in events[0][1]
