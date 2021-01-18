from typing import Optional

from pulumi import ComponentResource, InvokeOptions, Output, ResourceOptions, log
from pulumi_gcp import (
    cloudrun,
    compute,
    organizations,
    projects,
    pubsub,
    serviceaccount,
    storage,
)
from pulumi_gcp.storage import AwaitableGetProjectServiceAccountResult


class BucketWithNotificationArgs:
    """Creates a Bucket whose writes determine notifications on a Google PubSub Topic
    :param bucket_resource_name: The name of the Google Object Storage bucket to create
    :param gcp_project: The owning gcp project
    :param topic_resource_name_suffix: The suffix to append to the bucket name to create the topic
    """

    bucket_resource_name: str
    gcp_project: organizations.Project
    topic_resource_name_suffix: str

    def __init__(
        self,
        gcp_project: organizations.Project,
        bucket_resource_name: str,
        topic_resource_name_suffix: str,
    ):
        self.bucket_resource_name = bucket_resource_name
        self.gcp_project = gcp_project
        self.topic_resource_name_suffix = topic_resource_name_suffix


class BucketWithNotification(ComponentResource):

    bucket: storage.Bucket

    topic: pubsub.Topic

    gcs_default_project_service_account_topicbindingtopic_iambinding: pubsub.TopicIAMBinding

    notification: storage.Notification

    def _get_storage_project_service_account(
        self, project_id: str, opts: Optional[ResourceOptions]
    ) -> AwaitableGetProjectServiceAccountResult:
        """Retrieve the default project service account for Cloud storage"""
        invoke_opts = None
        if opts is not None:
            invoke_opts = InvokeOptions(provider=opts.provider)
        return storage.get_project_service_account(project=project_id, opts=invoke_opts)

    def __init__(
        self, name: str, args: BucketWithNotificationArgs, opts: ResourceOptions = None
    ):

        super().__init__("unopac:modules:BucketWithNotification", name, {}, opts)

        log.info(
            f"Trying to get project default service account for new project with {args.gcp_project}"
        )

        self.bucket = storage.Bucket(
            args.bucket_resource_name,
            project=args.gcp_project.project_id,
            opts=opts,
        )

        gcs_account = args.gcp_project.project_id.apply(
            lambda project_id: self._get_storage_project_service_account(
                project_id, opts
            )
        )

        self.topic = pubsub.Topic(
            f"{args.bucket_resource_name}-{args.topic_resource_name_suffix}",
            project=args.gcp_project.project_id,
            opts=opts,
        )

        self.gcs_default_project_service_account_topicbindingtopic_iambinding = (
            pubsub.TopicIAMBinding(
                f"{name}-default-project-service-account-topic-iam-binding",
                topic=self.topic.id,
                role="roles/pubsub.publisher",
                members=[f"serviceAccount:{gcs_account.email_address}"],
                opts=opts,
            )
        )

        self.pubsub_accountcreator_policy_binding = projects.IAMMember(
            resource_name="project-service-account-pubsub-serviceAccount-tokenCreator",
            project=args.gcp_project.project_id,
            member=Output.concat(
                "serviceAccount:service-",
                args.gcp_project.number,
                "@gcp-sa-pubsub.iam.gserviceaccount.com",
            ),
            role="roles/iam.serviceAccountTokenCreator",
        )

        self.notification = storage.Notification(
            f"{args.bucket_resource_name}-notification",
            bucket=self.bucket.name,
            payload_format="JSON_API_V1",
            topic=self.topic.id,
            event_types=[
                "OBJECT_FINALIZE",
                "OBJECT_METADATA_UPDATE",
            ],
            custom_attributes={
                "new-attribute": "new-attribute-value",
            },
            opts=opts,
        )
