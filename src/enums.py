from enum import Enum


class UserSubscribePlan(str, Enum):
    BASIC = 'basic'
    PLUS = 'plus'
    PRO = 'pro'


class UserScope(str, Enum):
    USER = 'user'
    ADMIN = 'admin'


class FileVisibility(str, Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'
