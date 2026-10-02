import json
from pathlib import Path


REPORT_DIRECTORY = Path("reports")
REPORT_FILE = REPORT_DIRECTORY / "report.json"


def generate_json_report(
    stopped_instances,
    unattached_volumes,
    old_snapshots,
    low_cpu_instances,
):
    """Create a JSON report containing resource findings."""

    report = {
        "stopped_instances": len(stopped_instances),
        "unattached_volumes": len(unattached_volumes),
        "old_snapshots": len(old_snapshots),
        "low_cpu_instances": len(low_cpu_instances),
    }

    REPORT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    with REPORT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
        )

    return report


if __name__ == "__main__":

    report = generate_json_report(
        stopped_instances=[],
        unattached_volumes=[],
        old_snapshots=[],
        low_cpu_instances=[],
    )

    print("\n=== JSON REPORT ===")
    print(json.dumps(report, indent=2))
    print(f"\nReport saved to: {REPORT_FILE}")