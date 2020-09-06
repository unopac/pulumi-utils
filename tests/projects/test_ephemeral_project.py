import pulumi

from pulumi import Output, Input
from tests.pulumi_mocks import PulumiMocks


pulumi.runtime.set_mocks(PulumiMocks())

# noqa: E402
from pulumi_utils.projects.ephemeral_project import Project, ProjectArgs


@pulumi.runtime.test
def test_ephemeral_project():
    project_name = "my-project-name"
    root_project_name = "root-project-name"
    organization_name = "root-organization-name"
    args = ProjectArgs(project_name, root_project_name, organization_name)
    project = Project("name", args)

    def test_properties(args):
        new_project_id = args
        assert new_project_id == project_name

    Output.all(project.new_project_id).apply(test_properties)
