from datetime import datetime, timedelta, timezone

from src.aws_clients import get_cloudwatch_client
from src.config import load_config


METRIC_NAME = "CPUUtilization"
NAMESPACE = "AWS/EC2"
PERIOD = 3600


def get_average_cpu(instance_id):
    """Get average CPU utilization using configured lookback period."""

    config = load_config()

    lookback_days = config["cloudwatch"]["lookback_days"]

    cloudwatch = get_cloudwatch_client()

    end_time = datetime.now(timezone.utc)

    start_time = end_time - timedelta(
        days=lookback_days
    )

    response = cloudwatch.get_metric_statistics(
        Namespace=NAMESPACE,
        MetricName=METRIC_NAME,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": instance_id,
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=PERIOD,
        Statistics=["Average"],
    )

    datapoints = response.get(
        "Datapoints",
        []
    )

    if not datapoints:
        return None

    total = sum(
        datapoint["Average"]
        for datapoint in datapoints
    )

    average_cpu = total / len(datapoints)

    return average_cpu


if __name__ == "__main__":

    instance_id = input(
        "Enter the EC2 Instance ID: "
    ).strip()

    config = load_config()

    lookback_days = config["cloudwatch"]["lookback_days"]

    average_cpu = get_average_cpu(
        instance_id
    )

    print("\n=== CLOUDWATCH CPU REPORT ===")

    print(
        f"Instance ID: {instance_id}"
    )

    print(
        "Metric: CPUUtilization"
    )

    print(
        f"Period: Last {lookback_days} days"
    )

    if average_cpu is None:

        print(
            "No CPU datapoints found."
        )

    else:

        print(
            f"Average CPU: "
            f"{average_cpu:.2f}%"
        )