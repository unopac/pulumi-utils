import pulumi
from unittest import mock


class PulumiMocks(pulumi.runtime.Mocks):
    call_mock = mock.MagicMock()

    def __init__(self):
        pass

    def new_resource(self, type_, name, inputs, provider, id_):
        return [name + "_id", inputs]

    def call(self, token, args, provider):
        import pdb

        pdb.set_trace()
        return {}
