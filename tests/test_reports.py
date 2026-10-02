import csv
import json

from src import json_reporter
from src import csv_reporter
from src import text_reporter


def test_json_report(tmp_path, monkeypatch):
    """Test JSON report generation."""

    report_directory = tmp_path / "reports"
    report_file = report_directory / "report.json"

    monkeypatch.setattr(
        json_reporter,
        "REPORT_DIRECTORY",
        report_directory,
    )

    monkeypatch.setattr(
        json_reporter,
        "REPORT_FILE",
        report_file,
    )

    result = json_reporter.generate_json_report(
        stopped_instances=[
            {"instance_id": "i-123"}
        ],
        unattached_volumes=[
            {"volume_id": "vol-123"}
        ],
        old_snapshots=[
            {"snapshot_id": "snap-123"}
        ],
        low_cpu_instances=[
            {"instance_id": "i-456"}
        ],
    )

    assert result["stopped_instances"] == 1
    assert result["unattached_volumes"] == 1
    assert result["old_snapshots"] == 1
    assert result["low_cpu_instances"] == 1

    assert report_file.exists()

    with report_file.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    assert data["stopped_instances"] == 1


def test_csv_report(tmp_path, monkeypatch):
    """Test CSV report generation."""

    report_directory = tmp_path / "reports"
    report_file = report_directory / "report.csv"

    monkeypatch.setattr(
        csv_reporter,
        "REPORT_DIRECTORY",
        report_directory,
    )

    monkeypatch.setattr(
        csv_reporter,
        "REPORT_FILE",
        report_file,
    )

    result = csv_reporter.generate_csv_report(
        stopped_instances=[
            {
                "instance_id": "i-123",
                "state": "stopped",
            }
        ],
        unattached_volumes=[
            {
                "volume_id": "vol-123",
                "state": "available",
            }
        ],
        old_snapshots=[
            {
                "snapshot_id": "snap-123",
                "age_days": 100,
            }
        ],
        low_cpu_instances=[
            {
                "instance_id": "i-456",
            }
        ],
    )

    assert result == report_file
    assert report_file.exists()

    with report_file.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 4
    assert rows[0]["Type"] == "EC2"
    assert rows[1]["Type"] == "EBS"
    assert rows[2]["Type"] == "Snapshot"
    assert rows[3]["Type"] == "EC2"


def test_text_report(tmp_path, monkeypatch):
    """Test human-readable report generation."""

    report_directory = tmp_path / "reports"
    report_file = report_directory / "summary.txt"

    monkeypatch.setattr(
        text_reporter,
        "REPORT_DIRECTORY",
        report_directory,
    )

    monkeypatch.setattr(
        text_reporter,
        "REPORT_FILE",
        report_file,
    )

    result = text_reporter.generate_text_report(
        stopped_instances=[
            {"instance_id": "i-123"}
        ],
        unattached_volumes=[
            {"volume_id": "vol-123"}
        ],
        old_snapshots=[
            {"snapshot_id": "snap-123"}
        ],
        low_cpu_instances=[
            {"instance_id": "i-456"}
        ],
    )

    assert result == report_file
    assert report_file.exists()

    content = report_file.read_text(
        encoding="utf-8"
    )

    assert "AWS COST & IDLE RESOURCE REPORT" in content
    assert "1 stopped instances found" in content
    assert "1 unattached volumes found" in content
    assert "1 snapshots older than configured threshold" in content
    assert "1 low-utilization instances detected" in content