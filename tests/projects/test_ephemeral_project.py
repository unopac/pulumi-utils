import pulumi
from pulumi import Input, Output

from tests.pulumi_mocks import PulumiMocks


def call_side_effect(token: str, args: dict, provider: str):
    return {}


pulumi.runtime.set_mocks(PulumiMocks())


from pulumi_utils.projects.ephemeral_project import Project, ProjectArgs  # noqa: E402


@pulumi.runtime.test
def test_ephemeral_project():
    project_name = "my-project-name"
    root_project_name = "root-project-name"
    organization_name = "root-organization-name"
    args = ProjectArgs(project_name, root_project_name, organization_name)
    project = Project("name", args)

    def test_properties(args):
        new_project_id = args[0]
        assert new_project_id == project_name

    Output.all(project.new_project_id).apply(test_properties)
