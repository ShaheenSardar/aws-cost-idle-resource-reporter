from pathlib import Path


REPORT_DIRECTORY = Path("reports")
REPORT_FILE = REPORT_DIRECTORY / "summary.txt"


def generate_text_report(
    stopped_instances,
    unattached_volumes,
    old_snapshots,
    low_cpu_instances,
):
    """Generate a human-readable AWS resource report."""

    REPORT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    report = f"""
AWS COST & IDLE RESOURCE REPORT
================================

EC2
{len(stopped_instances)} stopped instances found

EBS
{len(unattached_volumes)} unattached volumes found

Snapshots
{len(old_snapshots)} snapshots older than configured threshold

CloudWatch
{len(low_cpu_instances)} low-utilization instances detected
"""

    with REPORT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        file.write(report.strip() + "\n")

    return REPORT_FILE


if __name__ == "__main__":

    report_file = generate_text_report(
        stopped_instances=[],
        unattached_volumes=[],
        old_snapshots=[],
        low_cpu_instances=[],
    )

    print("\n=== HUMAN-READABLE REPORT ===")
    print(f"Report saved to: {report_file}")