import csv
from pathlib import Path


REPORT_DIRECTORY = Path("reports")
REPORT_FILE = REPORT_DIRECTORY / "report.csv"


def generate_csv_report(
    stopped_instances,
    unattached_volumes,
    old_snapshots,
    low_cpu_instances,
):
    """Generate a CSV report containing AWS resource findings."""

    REPORT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = []

    # -----------------------------
    # Stopped EC2
    # -----------------------------

    for instance in stopped_instances:

        rows.append(
            {
                "Type": "EC2",
                "Resource": instance["instance_id"],
                "Status": instance["state"],
                "Finding": "Potential waste - stopped instance",
            }
        )

    # -----------------------------
    # Unattached EBS
    # -----------------------------

    for volume in unattached_volumes:

        rows.append(
            {
                "Type": "EBS",
                "Resource": volume["volume_id"],
                "Status": volume["state"],
                "Finding": "Unattached volume",
            }
        )

    # -----------------------------
    # Old Snapshots
    # -----------------------------

    for snapshot in old_snapshots:

        rows.append(
            {
                "Type": "Snapshot",
                "Resource": snapshot["snapshot_id"],
                "Status": f"{snapshot['age_days']} days",
                "Finding": "Old snapshot",
            }
        )

    # -----------------------------
    # Low CPU EC2
    # -----------------------------

    for instance in low_cpu_instances:

        rows.append(
            {
                "Type": "EC2",
                "Resource": instance["instance_id"],
                "Status": "running",
                "Finding": "Low CPU utilization",
            }
        )

    # -----------------------------
    # Write CSV
    # -----------------------------

    with REPORT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        fieldnames = [
            "Type",
            "Resource",
            "Status",
            "Finding",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    return REPORT_FILE


if __name__ == "__main__":

    report_file = generate_csv_report(
        stopped_instances=[],
        unattached_volumes=[],
        old_snapshots=[],
        low_cpu_instances=[],
    )

    print("\n=== CSV REPORT ===")
    print(f"Report saved to: {report_file}")