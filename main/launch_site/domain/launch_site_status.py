from enum import Enum

class LaunchSiteStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    MAINTENANCE = "MAINTENANCE"
    CLOSED = "CLOSED"

