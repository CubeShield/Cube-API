from typing import TYPE_CHECKING

import aiohttp
from fastapi.params import Depends

from app.core.config import get_settings
from app.integrations.base_integration import BaseIntegration
from app.schemas.content_schema import CompiledContent, TypedContent
from app.schemas.integration_schema import IntegrationType
from app.services.mod.mod_content_cache_service import (
    ModContentCacheService,
    get_mod_cache_service,
)
from app.services.resourcepack.resourcepack_content_cache_service import (
    ResourcepackContentCacheService,
    get_resourcepack_content_cache_service,
)

if TYPE_CHECKING:
    from app.services.cache_service import CacheService


class CurseforgeIntegration(BaseIntegration):
    BASE_URL = "https://api.curseforge.com/v1"
    API_KEY = get_settings().curseforge_api_key
    integration_type = IntegrationType.curseforge

    async def get_content(self, content: TypedContent) -> CompiledContent:
        url = self.BASE_URL + f"/mods/{content.project}/files/{content.version}"
        headers = {"Accept": "application/json", "x-api-key": self.API_KEY}

        async with aiohttp.ClientSession() as session, session.get(url, headers=headers) as response:
            if response.status != 200:
                raise Exception(f"{self.__repr__()} is not reachable")
            data = (await response.json()).get("data")
            if not data:
                raise Exception(f"{self.__repr__()} is empty")
            return CompiledContent(file=data.get("fileName"), url=data.get("downloadUrl"))


async def get_curseforge_integration(
    mod_content_cache_service: ModContentCacheService = Depends(get_mod_cache_service),
    resourcepack_content_cache_service: ResourcepackContentCacheService = Depends(
        get_resourcepack_content_cache_service
    ),
) -> CurseforgeIntegration:
    cache_services: list[CacheService] = [
        mod_content_cache_service,
        resourcepack_content_cache_service,
    ]
    return CurseforgeIntegration(cache_services)
