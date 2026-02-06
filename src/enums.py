from enum import StrEnum


class UserSubscribePlan(StrEnum):
    BASIC = 'basic'
    PLUS = 'plus'
    PRO = 'pro'


class UserScope(StrEnum):
    USER = 'user'
    ADMIN = 'admin'


class FileVisibility(StrEnum):
    PUBLIC = 'public'
    PRIVATE = 'private'
