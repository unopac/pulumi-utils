import pulumi
from unittest import mock
from typing import Callable
from pulumi_gcp.organizations import GetOrganizationResult


class PulumiMocks(pulumi.runtime.Mocks):
    call_mock = mock.MagicMock()

    def __init__(self):
        self.call_mock.side_effect = self.call_mocked

    def new_resource(self, type_, name, inputs, provider, id_):
        return [name + "_id", inputs]

    def call(self, token, args, provider):
        return self.call_mock(token, args, provider)

    def call_mocked(self, token, args, provider):
        import pdb

        if token == "gcp:organizations/getOrganization:getOrganization":
            return self.mock_get_organization(args)
        pdb.set_trace()
        return {}

    def mock_get_organization(self, args):
        return GetOrganizationResult(
            create_time=None,
            directory_customer_id=None,
            domain=None,
            id=None,
            lifecycle_state=None,
            name=None,
            org_id="my-org-id",
            organization=None,
        )
