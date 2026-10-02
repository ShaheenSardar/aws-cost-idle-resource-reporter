from src.ec2_scanner import find_stopped_instances


def test_find_stopped_instances():
    instances = [
        {
            "instance_id": "i-123456",
            "instance_type": "t3.micro",
            "state": "stopped",
            "name": "test-server",
            "availability_zone": "us-east-1a",
            "tags": [],
        },
        {
            "instance_id": "i-789012",
            "instance_type": "t3.micro",
            "state": "running",
            "name": "web-server",
            "availability_zone": "us-east-1a",
            "tags": [],
        },
    ]

    stopped = find_stopped_instances(instances)

    assert len(stopped) == 1
    assert stopped[0]["instance_id"] == "i-123456"


def test_no_stopped_instances():
    instances = [
        {
            "instance_id": "i-123456",
            "instance_type": "t3.micro",
            "state": "running",
            "name": "web-server",
            "availability_zone": "us-east-1a",
            "tags": [],
        }
    ]

    stopped = find_stopped_instances(instances)

    assert len(stopped) == 0