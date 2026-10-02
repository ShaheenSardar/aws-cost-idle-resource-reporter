import argparse

from src.logger import get_logger
from src.error_handler import handle_aws_error
from src.config import load_config
from src.text_reporter import generate_text_report

from src.ec2_scanner import (
    scan_ec2_instances,
    find_stopped_instances,
)

from src.ebs_scanner import (
    scan_ebs_volumes,
    find_unattached_volumes,
)

from src.snapshot_scanner import (
    scan_snapshots,
    find_old_snapshots,
)

from src.cloudwatch_analyzer import get_average_cpu
from src.tag_filter import filter_resources
from src.json_reporter import generate_json_report
from src.csv_reporter import generate_csv_report


def parse_arguments():
    """Read command-line tag filters."""

    parser = argparse.ArgumentParser(
        description="AWS Cost & Idle Resource Reporter"
    )

    parser.add_argument(
        "--environment",
        choices=["dev", "prod"],
        help="Filter resources by Environment tag",
    )

    parser.add_argument(
        "--owner",
        help="Filter resources by Owner tag",
    )

    parser.add_argument(
        "--project",
        help="Filter resources by Project tag",
    )

    return parser.parse_args()


def build_filters(args):
    """Build tag filters from command-line arguments."""

    filters = {}

    if args.environment:
        filters["Environment"] = args.environment

    if args.owner:
        filters["Owner"] = args.owner

    if args.project:
        filters["Project"] = args.project

    return filters


def print_resource_tags(resource):
    """Convert resource tags into readable text."""

    tags = resource.get("tags", [])

    if not tags:
        return "No tags"

    return ", ".join(
        f"{tag['Key']}={tag['Value']}"
        for tag in tags
    )


def main():

    logger = get_logger()

    logger.info(
        "Starting AWS Cost & Idle Resource Reporter"
    )

    try:

        config = load_config()

        cpu_threshold = config[
            "cloudwatch"
        ][
            "cpu_threshold"
        ]

        snapshot_age_days = config[
            "snapshot_age_days"
        ]

        lookback_days = config[
            "cloudwatch"
        ][
            "lookback_days"
        ]

        args = parse_arguments()

        filters = build_filters(args)

        print(
            "\n========================================"
        )

        print(
            "       AWS COST & IDLE RESOURCE REPORT"
        )

        print(
            "========================================"
        )

        print(
            f"\nConfiguration:"
        )

        print(
            f"Snapshot age threshold : "
            f"{snapshot_age_days} days"
        )

        print(
            f"CloudWatch lookback   : "
            f"{lookback_days} days"
        )

        print(
            f"CPU threshold         : "
            f"{cpu_threshold}%"
        )

        if filters:

            print(
                "\nActive filters:"
            )

            for key, value in filters.items():

                print(
                    f"{key}={value}"
                )

            logger.info(
                f"Active tag filters: {filters}"
            )

        else:

            print(
                "\nNo tag filters specified."
            )

            print(
                "All resources will be analyzed."
            )

            logger.info(
                "No tag filters specified; "
                "analyzing all resources"
            )

        # ==============================
        # EC2
        # ==============================

        logger.info(
            "Scanning EC2 instances"
        )

        print(
            "\n[1] Scanning EC2 instances..."
        )

        ec2_resources = scan_ec2_instances()

        if filters:

            ec2_resources = filter_resources(
                ec2_resources,
                filters,
            )

        stopped_instances = (
            find_stopped_instances(
                ec2_resources
            )
        )

        print(
            f"Matching EC2 instances: "
            f"{len(ec2_resources)}"
        )

        print(
            f"Stopped EC2 instances: "
            f"{len(stopped_instances)}"
        )

        if stopped_instances:

            logger.warning(
                f"Found "
                f"{len(stopped_instances)} "
                f"stopped EC2 instance(s)"
            )

        for resource in ec2_resources:

            print(
                f"EC2: "
                f"{resource['instance_id']} | "
                f"Name: {resource['name']} | "
                f"State: {resource['state']} | "
                f"Tags: "
                f"{print_resource_tags(resource)}"
            )

        # ==============================
        # EBS
        # ==============================

        logger.info(
            "Scanning EBS volumes"
        )

        print(
            "\n[2] Scanning EBS volumes..."
        )

        ebs_resources = scan_ebs_volumes()

        if filters:

            ebs_resources = filter_resources(
                ebs_resources,
                filters,
            )

        unattached_volumes = (
            find_unattached_volumes(
                ebs_resources
            )
        )

        print(
            f"Matching EBS volumes: "
            f"{len(ebs_resources)}"
        )

        print(
            f"Unattached EBS volumes: "
            f"{len(unattached_volumes)}"
        )

        if unattached_volumes:

            logger.warning(
                f"Found "
                f"{len(unattached_volumes)} "
                f"unattached EBS volume(s)"
            )

        for resource in ebs_resources:

            print(
                f"EBS: "
                f"{resource['volume_id']} | "
                f"Size: {resource['size']} GiB | "
                f"State: {resource['state']} | "
                f"Tags: "
                f"{print_resource_tags(resource)}"
            )

        # ==============================
        # SNAPSHOTS
        # ==============================

        logger.info(
            "Scanning EBS snapshots"
        )

        print(
            "\n[3] Scanning EBS snapshots..."
        )

        snapshot_resources = scan_snapshots()

        if filters:

            snapshot_resources = filter_resources(
                snapshot_resources,
                filters,
            )

        old_snapshots = (
            find_old_snapshots(
                snapshot_resources
            )
        )

        print(
            f"Matching snapshots: "
            f"{len(snapshot_resources)}"
        )

        print(
            f"Old snapshots: "
            f"{len(old_snapshots)}"
        )

        if old_snapshots:

            logger.warning(
                f"Found "
                f"{len(old_snapshots)} "
                f"old EBS snapshot(s)"
            )

        for resource in snapshot_resources:

            print(
                f"Snapshot: "
                f"{resource['snapshot_id']} | "
                f"Age: "
                f"{resource['age_days']} days | "
                f"Tags: "
                f"{print_resource_tags(resource)}"
            )

        # ==============================
        # CLOUDWATCH
        # ==============================

        logger.info(
            "Analyzing CloudWatch CPU metrics"
        )

        print(
            "\n[4] Analyzing CloudWatch CPU..."
        )

        low_cpu_instances = []

        for instance in ec2_resources:

            instance_id = instance[
                "instance_id"
            ]

            average_cpu = get_average_cpu(
                instance_id
            )

            if average_cpu is None:

                print(
                    f"{instance_id}: "
                    f"No CPU datapoints found."
                )

                logger.info(
                    f"{instance_id}: "
                    f"No CPU datapoints found"
                )

            else:

                print(
                    f"{instance_id}: "
                    f"Average CPU = "
                    f"{average_cpu:.2f}%"
                )

                logger.info(
                    f"{instance_id}: "
                    f"Average CPU = "
                    f"{average_cpu:.2f}%"
                )

                if average_cpu < cpu_threshold:

                    low_cpu_instances.append(
                        instance
                    )

        print(
            f"Low CPU instances "
            f"(< {cpu_threshold}%): "
            f"{len(low_cpu_instances)}"
        )

        if low_cpu_instances:

            logger.warning(
                f"Found "
                f"{len(low_cpu_instances)} "
                f"low-utilization "
                f"EC2 instance(s)"
            )

        # ==============================
        # REPORTS
        # ==============================

        logger.info(
            "Generating JSON report"
        )

        report = generate_json_report(
            stopped_instances=stopped_instances,
            unattached_volumes=unattached_volumes,
            old_snapshots=old_snapshots,
            low_cpu_instances=low_cpu_instances,
        )

        logger.info(
            "Generating CSV report"
        )

        csv_file = generate_csv_report(
            stopped_instances=stopped_instances,
            unattached_volumes=unattached_volumes,
            old_snapshots=old_snapshots,
            low_cpu_instances=low_cpu_instances,
        )

        print(
            "\nCSV report generated:"
        )

        print(csv_file)

        logger.info(
            "Generating human-readable report"
        )

        text_file = generate_text_report(
            stopped_instances=stopped_instances,
            unattached_volumes=unattached_volumes,
            old_snapshots=old_snapshots,
            low_cpu_instances=low_cpu_instances,
        )

        print(
            "\nHuman-readable report generated:"
        )

        print(text_file)

        # ==============================
        # SUMMARY
        # ==============================

        print(
            "\n========================================"
        )

        print(
            "                SUMMARY"
        )

        print(
            "========================================"
        )

        print(
            f"Stopped EC2         : "
            f"{report['stopped_instances']}"
        )

        print(
            f"Unattached EBS      : "
            f"{report['unattached_volumes']}"
        )

        print(
            f"Old snapshots       : "
            f"{report['old_snapshots']}"
        )

        print(
            f"Low CPU instances   : "
            f"{report['low_cpu_instances']}"
        )

        print(
            "\nJSON report generated:"
        )

        print(
            "reports/report.json"
        )

        print(
            "\nCSV report generated:"
        )

        print(
            "reports/report.csv"
        )

        print(
            "\nHuman-readable report generated:"
        )

        print(
            "reports/summary.txt"
        )

        print(
            "\n========================================"
        )

        print(
            "             REPORT COMPLETE"
        )

        print(
            "========================================"
        )

        logger.info(
            "Scan completed successfully"
        )

    except Exception as error:

        handle_aws_error(
            error,
            logger,
        )

        print(
            "\nScan failed. "
            "Check logs/app.log for details."
        )


if __name__ == "__main__":
    main()