from datetime import datetime, timezone

from src.aws_clients import get_ec2_client
from src.config import load_config


def scan_snapshots():
    """Scan all EBS snapshots owned by this AWS account."""
    ec2 = get_ec2_client()

    snapshots = []

    paginator = ec2.get_paginator("describe_snapshots")

    for page in paginator.paginate(OwnerIds=["self"]):
        for snapshot in page.get("Snapshots", []):

            start_time = snapshot.get("StartTime")

            if start_time:
                age_days = (
                    datetime.now(timezone.utc) - start_time
                ).days
            else:
                age_days = None

            snapshot_info = {
                "snapshot_id": snapshot.get("SnapshotId"),
                "volume_id": snapshot.get("VolumeId"),
                "volume_size": snapshot.get("VolumeSize"),
                "state": snapshot.get("State"),
                "start_time": start_time,
                "age_days": age_days,
                "tags": snapshot.get("Tags", []),
            }

            snapshots.append(snapshot_info)

    return snapshots


def find_old_snapshots(snapshots):
    """Find snapshots older than the configured age threshold."""

    config = load_config()

    threshold_days = config["snapshot_age_days"]

    return [
        snapshot
        for snapshot in snapshots
        if snapshot["age_days"] is not None
        and snapshot["age_days"] > threshold_days
    ]


if __name__ == "__main__":
    all_snapshots = scan_snapshots()

    old_snapshots = find_old_snapshots(all_snapshots)

    config = load_config()
    threshold_days = config["snapshot_age_days"]

    print("\n=== EBS SNAPSHOT REPORT ===")

    print(f"\nTotal snapshots found: {len(all_snapshots)}")

    print(
        f"Snapshots older than "
        f"{threshold_days} days: "
        f"{len(old_snapshots)}"
    )

    print("\n--- All Snapshots ---")

    for snapshot in all_snapshots:
        print(
            f"ID: {snapshot['snapshot_id']} | "
            f"Volume: {snapshot['volume_id']} | "
            f"Size: {snapshot['volume_size']} GiB | "
            f"State: {snapshot['state']} | "
            f"Created: {snapshot['start_time']} | "
            f"Age: {snapshot['age_days']} days"
        )

    print("\n--- Old Snapshots ---")

    for snapshot in old_snapshots:
        print(
            f"ID: {snapshot['snapshot_id']} | "
            f"Created: {snapshot['start_time']} | "
            f"Age: {snapshot['age_days']} days"
        )