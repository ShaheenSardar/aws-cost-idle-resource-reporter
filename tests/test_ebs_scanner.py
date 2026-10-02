from src.ebs_scanner import find_unattached_volumes


def test_find_unattached_volumes():
    volumes = [
        {
            "volume_id": "vol-123456",
            "size": 8,
            "volume_type": "gp3",
            "state": "available",
            "availability_zone": "us-east-1a",
            "encrypted": True,
            "attached_instance": None,
            "tags": [],
        },
        {
            "volume_id": "vol-789012",
            "size": 8,
            "volume_type": "gp3",
            "state": "in-use",
            "availability_zone": "us-east-1a",
            "encrypted": True,
            "attached_instance": "i-123456",
            "tags": [],
        },
    ]

    unattached = find_unattached_volumes(volumes)

    assert len(unattached) == 1
    assert unattached[0]["volume_id"] == "vol-123456"


def test_no_unattached_volumes():
    volumes = [
        {
            "volume_id": "vol-789012",
            "size": 8,
            "volume_type": "gp3",
            "state": "in-use",
            "availability_zone": "us-east-1a",
            "encrypted": True,
            "attached_instance": "i-123456",
            "tags": [],
        }
    ]

    unattached = find_unattached_volumes(volumes)

    assert len(unattached) == 0