from src.ec2_scanner import scan_ec2_instances, find_stopped_instances
from src.ebs_scanner import scan_ebs_volumes, find_unattached_volumes
from src.snapshot_scanner import scan_snapshots, find_old_snapshots
from src.cloudwatch_analyzer import get_average_cpu


def generate_report():
    """Generate a combined AWS resource report."""

    print("\n========================================")
    print("       AWS COST & IDLE RESOURCE REPORT")
    print("========================================")

    # -----------------------------
    # EC2
    # -----------------------------

    print("\n[1] Scanning EC2 instances...")

    ec2_instances = scan_ec2_instances()
    stopped_instances = find_stopped_instances(ec2_instances)

    print(f"Total EC2 instances: {len(ec2_instances)}")
    print(f"Stopped EC2 instances: {len(stopped_instances)}")

    # -----------------------------
    # EBS
    # -----------------------------

    print("\n[2] Scanning EBS volumes...")

    ebs_volumes = scan_ebs_volumes()
    unattached_volumes = find_unattached_volumes(ebs_volumes)

    print(f"Total EBS volumes: {len(ebs_volumes)}")
    print(f"Unattached EBS volumes: {len(unattached_volumes)}")

    # -----------------------------
    # Snapshots
    # -----------------------------

    print("\n[3] Scanning EBS snapshots...")

    snapshots = scan_snapshots()
    old_snapshots = find_old_snapshots(snapshots)

    print(f"Total snapshots: {len(snapshots)}")
    print(f"Old snapshots: {len(old_snapshots)}")

    # -----------------------------
    # CloudWatch
    # -----------------------------

    print("\n[4] Analyzing CloudWatch CPU...")

    for instance in ec2_instances:

        instance_id = instance["instance_id"]

        average_cpu = get_average_cpu(instance_id)

        if average_cpu is None:
            print(
                f"{instance_id}: No CPU datapoints found."
            )
        else:
            print(
                f"{instance_id}: "
                f"Average CPU = {average_cpu:.2f}%"
            )

    # -----------------------------
    # Summary
    # -----------------------------

    print("\n========================================")
    print("                 SUMMARY")
    print("========================================")

    print(f"EC2 instances       : {len(ec2_instances)}")
    print(f"Stopped EC2         : {len(stopped_instances)}")
    print(f"EBS volumes         : {len(ebs_volumes)}")
    print(f"Unattached EBS      : {len(unattached_volumes)}")
    print(f"EBS snapshots       : {len(snapshots)}")
    print(f"Old snapshots       : {len(old_snapshots)}")

    print("\n========================================")
    print("              REPORT COMPLETE")
    print("========================================")


if __name__ == "__main__":
    generate_report()