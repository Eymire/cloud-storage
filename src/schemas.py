from datetime import datetime

from pydantic import BaseModel

from src.enums import FileVisibility, UserScope, UserSubscribePlan


class User(BaseModel):
    id: int
    name: str
    email: str
    subscribe_plan: UserSubscribePlan
    scope: UserScope
    password_hash: str
    used_storage: int
    created_at: datetime


class File(BaseModel):
    id: int
    user_id: int
    name: str
    stored_name: str
    size: int
    content_type: str
    visibility: FileVisibility
    created_at: datetime
