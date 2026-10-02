def get_resource_tags(tags):
    """Convert AWS tag list into a dictionary."""

    return {
        tag["Key"]: tag["Value"]
        for tag in tags or []
    }


def resource_matches_filter(tags, filters):
    """Check whether a resource matches all requested tag filters."""

    resource_tags = get_resource_tags(tags)

    for key, expected_value in filters.items():

        if resource_tags.get(key) != expected_value:
            return False

    return True


def filter_resources(resources, filters):
    """Return only resources matching the requested tag filters."""

    filtered_resources = []

    for resource in resources:

        if resource_matches_filter(
            resource.get("tags", []),
            filters,
        ):
            filtered_resources.append(resource)

    return filtered_resources