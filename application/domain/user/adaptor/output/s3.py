from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4

from application.domain.user.model.vo import PreSignedUrl
from application.domain.user.use_case.port.output import UserS3OutputPort

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


class UserS3OutputAdaptor(UserS3OutputPort):
    def __init__(self, *, s3_client: "S3Client", bucket_name: str):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    async def make_face_upload_pre_signed_url(self, *, user_id: int) -> PreSignedUrl:
        now = datetime.now(tz=timezone.utc)
        key = f"face_verification/{now.year}/{now.month}/{now.day}/{uuid4()}/{user_id}/video.mp4"
        url = self.s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": key,
            },
        )
        return PreSignedUrl(
            pre_signed_url=url,
            key=key,
        )
