from botocore.exceptions import (
    ClientError,
    NoCredentialsError,
    NoRegionError,
    EndpointConnectionError,
)


def handle_aws_error(error, logger):
    """Handle common AWS and Boto3 errors."""

    if isinstance(error, NoCredentialsError):

        logger.error(
            "AWS credentials were not found."
        )

        print(
            "\nERROR: AWS credentials were not found."
        )

        print(
            "Check your AWS profile and credentials."
        )

    elif isinstance(error, NoRegionError):

        logger.error(
            "AWS region was not configured."
        )

        print(
            "\nERROR: AWS region was not configured."
        )

    elif isinstance(error, EndpointConnectionError):

        logger.error(
            "Unable to connect to the AWS endpoint."
        )

        print(
            "\nERROR: Unable to connect to AWS."
        )

        print(
            "Check your network connection and AWS region."
        )

    elif isinstance(error, ClientError):

        error_code = error.response.get(
            "Error",
            {}
        ).get(
            "Code",
            "Unknown",
        )

        if error_code == "AccessDenied":

            logger.error(
                "AWS API request was denied: "
                "AccessDenied"
            )

            print(
                "\nERROR: AWS access was denied."
            )

            print(
                "Check IAM permissions."
            )

        elif error_code in (
            "Throttling",
            "ThrottlingException",
            "RequestLimitExceeded",
        ):

            logger.error(
                "AWS API request was throttled."
            )

            print(
                "\nERROR: AWS API request was throttled."
            )

            print(
                "Too many requests were sent to AWS."
            )

        else:

            logger.error(
                f"AWS API error: {error_code}"
            )

            print(
                f"\nERROR: AWS API error: "
                f"{error_code}"
            )

    else:

        logger.exception(
            "Unexpected application error"
        )

        print(
            "\nERROR: An unexpected error occurred."
        )