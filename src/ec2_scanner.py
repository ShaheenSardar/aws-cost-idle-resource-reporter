from src.aws_clients import get_ec2_client


def scan_ec2_instances():
    """Scan all EC2 instances in the configured AWS region."""

    ec2 = get_ec2_client()
    instances = []

    paginator = ec2.get_paginator("describe_instances")

    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):

                tags = {
                    tag["Key"]: tag["Value"]
                    for tag in instance.get("Tags", [])
                }

                instance_info = {
                    "instance_id": instance.get("InstanceId"),
                    "instance_type": instance.get("InstanceType"),
                    "state": instance.get("State", {}).get("Name"),
                    "name": tags.get("Name", "N/A"),
                    "availability_zone": instance.get(
                        "Placement", {}
                    ).get("AvailabilityZone", "N/A"),
                    "tags": instance.get("Tags", []),
                }

                instances.append(instance_info)

    return instances


def find_stopped_instances(instances):
    """Find EC2 instances that are currently stopped."""

    return [
        instance
        for instance in instances
        if instance["state"] == "stopped"
    ]


if __name__ == "__main__":

    all_instances = scan_ec2_instances()
    stopped_instances = find_stopped_instances(all_instances)

    print("\n=== EC2 RESOURCE REPORT ===")

    print(f"\nTotal instances found: {len(all_instances)}")
    print(f"Stopped instances: {len(stopped_instances)}")

    print("\n--- All EC2 Instances ---")

    for instance in all_instances:
        print(
            f"ID: {instance['instance_id']} | "
            f"Name: {instance['name']} | "
            f"Type: {instance['instance_type']} | "
            f"State: {instance['state']} | "
            f"AZ: {instance['availability_zone']}"
        )

    print("\n--- Stopped EC2 Instances ---")

    for instance in stopped_instances:
        print(
            f"ID: {instance['instance_id']} | "
            f"Name: {instance['name']} | "
            f"Type: {instance['instance_type']} | "
            f"State: {instance['state']}"
        )