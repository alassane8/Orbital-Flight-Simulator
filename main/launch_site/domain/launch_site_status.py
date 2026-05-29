from enum import Enum


class LaunchSiteStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    AVAILABLE = "AVAILABLE"
    MAINTENANCE = "MAINTENANCE"
    CLOSED = "CLOSED"