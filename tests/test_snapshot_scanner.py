from datetime import datetime, timedelta, timezone

from src.snapshot_scanner import find_old_snapshots


def test_find_old_snapshots(monkeypatch):
    old_snapshot_time = (
        datetime.now(timezone.utc)
        - timedelta(days=100)
    )

    snapshots = [
        {
            "snapshot_id": "snap-old-123",
            "volume_id": "vol-123",
            "volume_size": 8,
            "state": "completed",
            "start_time": old_snapshot_time,
            "age_days": 100,
            "tags": [],
        },
        {
            "snapshot_id": "snap-new-456",
            "volume_id": "vol-456",
            "volume_size": 8,
            "state": "completed",
            "start_time": datetime.now(timezone.utc),
            "age_days": 10,
            "tags": [],
        },
    ]

    old_snapshots = find_old_snapshots(snapshots)

    assert len(old_snapshots) == 1
    assert old_snapshots[0]["snapshot_id"] == "snap-old-123"


def test_no_old_snapshots():
    snapshots = [
        {
            "snapshot_id": "snap-new-456",
            "volume_id": "vol-456",
            "volume_size": 8,
            "state": "completed",
            "start_time": datetime.now(timezone.utc),
            "age_days": 10,
            "tags": [],
        }
    ]

    old_snapshots = find_old_snapshots(snapshots)

    assert len(old_snapshots) == 0
    