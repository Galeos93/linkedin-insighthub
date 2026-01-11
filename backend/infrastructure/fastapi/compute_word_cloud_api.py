from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass

from fastapi import Depends
from fastapi.responses import Response
from domain.entities.user_id import UserId
from application.use_cases.compute_word_cloud import ComputeWordCloud
from infrastructure.fastapi.common import get_anonymous_user


class ComputeWordCloudAPIBase(ABC):
    @abstractmethod
    async def compute_word_cloud(self, user_id: UserId) -> Any:
        pass


@dataclass
class ComputeWordCloudAPIImpl(ComputeWordCloudAPIBase):
    compute_word_cloud_use_case: ComputeWordCloud

    async def compute_word_cloud(self, user_id: UserId = Depends(get_anonymous_user)) -> Response:
        image_bytes = self.compute_word_cloud_use_case.compute(user_id=user_id)
        return Response(content=image_bytes, media_type="image/png")
