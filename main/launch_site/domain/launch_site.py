from datetime import datetime
from dataclasses import dataclass, field
from launch_site.domain.launch_site_status import LaunchSiteStatus

@dataclass
class LaunchSite:
    id: str 
    code: str
    status: LaunchSiteStatus
    lat: float
    lon: float
    name: str
    country: str
    operator: str

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)