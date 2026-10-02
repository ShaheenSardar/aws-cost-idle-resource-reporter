from src.tag_filter import resource_matches_filter


def test_environment_filter():

    tags = [
        {
            "Key": "Environment",
            "Value": "dev",
        },
        {
            "Key": "Owner",
            "Value": "Shaheen",
        },
    ]

    assert resource_matches_filter(
        tags,
        {"Environment": "dev"},
    )


def test_wrong_environment():

    tags = [
        {
            "Key": "Environment",
            "Value": "prod",
        }
    ]

    assert not resource_matches_filter(
        tags,
        {"Environment": "dev"},
    )