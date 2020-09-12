import pulumi_gcp
from pulumi import ComponentResource, Output, ResourceOptions
from pulumi_gcp import (
    cloudrun,
    compute,
    organizations,
    projects,
    pubsub,
    serviceaccount,
    storage,
)

from pulumi_utils.projects.ephemeral_project import Project



class BucketWithNotificationArgs:

    bucket_resource_name: str
    gcp_project: str
    topic_resource_name_suffix: str

    def __init__(
        self,
        gcp_project: Project,
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

    def __init__(
        self, name: str, args: BucketWithNotificationArgs, opts: ResourceOptions = None
    ):

        super().__init__("unopac:modules:BucketWithNotification", name, {}, opts)

        self.bucket = storage.Bucket(
            args.bucket_resource_name,
            project=args.gcp_project.new_project_id,
            opts=opts,
        )

        gcs_account = storage.get_project_service_account(
            project=args.gcp_project.new_project_id,
            opts=opts,
        )

        self.topic = pubsub.Topic(
            f"{args.bucket_resource_name}-{args.topic_resource_name_suffix}",
            project=args.gcp_project.new_project_id,
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
            project=args.gcp_project.new_project_id,
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
