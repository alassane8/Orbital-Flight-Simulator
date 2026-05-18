from datetime import datetime
from dataclasses import dataclass, field
from launch_site.domain.launch_site_status import LaunchSiteStatus

@dataclass
class LaunchSite:
    id: str 
    launch_site_code: str
    status: LaunchSiteStatus
    lat: float
    lon: float

    created_at: field(default_factory=datetime.now)
    updated_at: field(default_factory=datetime.now)