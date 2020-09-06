import pulumi

from pulumi import Output, Input
from tests.pulumi_mocks import PulumiMocks

pulumi.runtime.set_mocks(PulumiMocks())

# noqa: E402
from pulumi_utils.cloudrun.cross_project_docker_registry_access import (
    CrossProjectCloudRunAccess,
    CrossProjectCloudRunAccessArgs,
)


@pulumi.runtime.test
def test_cross_project_registry():
    bucket_name = "my-bucketname"
    target_project_number = "target_project_number"
    args = CrossProjectCloudRunAccessArgs(
        bucket_name, Output.from_input(target_project_number)
    )

    cloud_run_access = CrossProjectCloudRunAccess(
        "my-cloudrun-cross-registry-access", args, None
    )

    def test_properties(args):
        observed_bucket_name, observed_member = args
        assert observed_bucket_name == bucket_name
        assert observed_member == _cloudrun_service_account(target_project_number)

    return Output.all(
        cloud_run_access.bucket_policy.bucket, cloud_run_access.bucket_policy.member
    ).apply(test_properties)


def _cloudrun_service_account(project_number: str) -> str:
    return f"serviceAccount:service-{project_number}@serverless-robot-prod.iam.gserviceaccount.com"
