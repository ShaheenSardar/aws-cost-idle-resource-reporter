from src import cloudwatch_analyzer


class FakeCloudWatchClient:
    """Fake CloudWatch client for unit testing."""

    def get_metric_statistics(
        self,
        Namespace,
        MetricName,
        Dimensions,
        StartTime,
        EndTime,
        Period,
        Statistics,
    ):
        return {
            "Datapoints": [
                {"Average": 2.0},
                {"Average": 4.0},
                {"Average": 6.0},
            ]
        }


def test_get_average_cpu(monkeypatch):
    """Test average CPU calculation."""

    monkeypatch.setattr(
        cloudwatch_analyzer,
        "get_cloudwatch_client",
        lambda: FakeCloudWatchClient(),
    )

    average_cpu = cloudwatch_analyzer.get_average_cpu(
        "i-test123"
    )

    assert average_cpu == 4.0


def test_no_cpu_datapoints(monkeypatch):
    """Test behavior when CloudWatch returns no datapoints."""

    class EmptyCloudWatchClient:
        def get_metric_statistics(
            self,
            Namespace,
            MetricName,
            Dimensions,
            StartTime,
            EndTime,
            Period,
            Statistics,
        ):
            return {
                "Datapoints": []
            }

    monkeypatch.setattr(
        cloudwatch_analyzer,
        "get_cloudwatch_client",
        lambda: EmptyCloudWatchClient(),
    )

    average_cpu = cloudwatch_analyzer.get_average_cpu(
        "i-test123"
    )

    assert average_cpu is None
    