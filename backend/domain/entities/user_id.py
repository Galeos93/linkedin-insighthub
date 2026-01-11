from typing import NewType

from dataclasses import dataclass

UserId = NewType("UserId", str)


# @dataclass(frozen=True)
# class UserId:
#     id: str
