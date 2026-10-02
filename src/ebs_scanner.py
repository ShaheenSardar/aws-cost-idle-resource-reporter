from src.aws_clients import get_ec2_client


def scan_ebs_volumes():
    """Scan all EBS volumes in the configured AWS region."""

    ec2 = get_ec2_client()
    volumes = []

    paginator = ec2.get_paginator("describe_volumes")

    for page in paginator.paginate():
        for volume in page.get("Volumes", []):

            attachments = volume.get("Attachments", [])

            volume_info = {
                "volume_id": volume.get("VolumeId"),
                "size": volume.get("Size"),
                "volume_type": volume.get("VolumeType"),
                "state": volume.get("State"),
                "availability_zone": volume.get("AvailabilityZone"),
                "encrypted": volume.get("Encrypted"),
                "attached_instance": (
                    attachments[0].get("InstanceId")
                    if attachments
                    else None
                ),
                "tags": volume.get("Tags", []),
            }

            volumes.append(volume_info)

    return volumes


def find_unattached_volumes(volumes):
    """Find EBS volumes that are not attached to an EC2 instance."""

    return [
        volume
        for volume in volumes
        if volume["state"] == "available"
    ]


if __name__ == "__main__":

    all_volumes = scan_ebs_volumes()
    unattached_volumes = find_unattached_volumes(all_volumes)

    print("\n=== EBS RESOURCE REPORT ===")

    print(f"\nTotal EBS volumes found: {len(all_volumes)}")
    print(f"Unattached EBS volumes: {len(unattached_volumes)}")

    print("\n--- All EBS Volumes ---")

    for volume in all_volumes:
        print(
            f"ID: {volume['volume_id']} | "
            f"Size: {volume['size']} GiB | "
            f"Type: {volume['volume_type']} | "
            f"State: {volume['state']} | "
            f"AZ: {volume['availability_zone']} | "
            f"Encrypted: {volume['encrypted']} | "
            f"Instance: {volume['attached_instance']}"
        )

    print("\n--- Unattached EBS Volumes ---")

    for volume in unattached_volumes:
        print(
            f"ID: {volume['volume_id']} | "
            f"Size: {volume['size']} GiB | "
            f"Type: {volume['volume_type']} | "
            f"State: {volume['state']} | "
            f"AZ: {volume['availability_zone']}"
        )