import base64
from typing import Callable
from unittest import mock

import pulumi
from pulumi_gcp.organizations import GetOrganizationResult


class PulumiMocks(pulumi.runtime.Mocks):
    call_mock = mock.MagicMock()

    def __init__(self):
        self.call_mock.side_effect = self.call_mocked

    def new_resource(self, type_, name, inputs, provider, id_):
        if type_ == "gcp:serviceAccount/key:Key":
            inputs["private_key"] = str(
                base64.b64encode(b"example-private-key"), "utf-8"
            )
        return [name + "_id", inputs]

    def call(self, token, args, provider):
        return self.call_mock(token, args, provider)

    def call_mocked(self, token, args, provider):
        if token == "gcp:organizations/getOrganization:getOrganization":
            return self.mock_get_organization(args)

        return {}

    def mock_get_organization(self, args):
        return {"org_id": "my-org-id", "name": "my-org-fond", "id": "pippo"}

        #         return GetOrganizationResult(
        #     create_time=None,
        #     directory_customer_id=None,
        #     domain=None,
        #     id=None,
        #     lifecycle_state=None,
        #     name=None,
        #     org_id="my-org-id",
        #     organization=None,
        # )
