from app.core.config import Settings
from app.schemas.system import SystemInfoResponse


class SystemService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_info(self) -> SystemInfoResponse:
        return SystemInfoResponse(
            app_name=self.settings.app_name,
            version=self.settings.app_version,
            environment=self.settings.environment,
            debug=self.settings.debug,
        )
