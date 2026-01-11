from abc import ABC, abstractmethod
from fastapi import Depends
from typing import List
from dataclasses import dataclass

from domain.entities.user_id import UserId
from domain.entities.post import PostProjection
from application.use_cases.compute_projection import ComputeProjection
from infrastructure.fastapi.common import get_anonymous_user


class ComputeProjectionAPIBase(ABC):
    @abstractmethod
    async def compute_projection(self, user_id: UserId) -> List[PostProjection]:
        pass


@dataclass
class ComputeProjectionAPIImpl(ComputeProjectionAPIBase):
    compute_projection_use_case: ComputeProjection

    async def compute_projection(self, user_id: UserId = Depends(get_anonymous_user)) -> List[PostProjection]:
        projections = self.compute_projection_use_case.compute(user_id=user_id)
        return projections
