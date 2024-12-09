from typing import TYPE_CHECKING

import aiohttp
from fastapi.params import Depends

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


class ModrinthIntegration(BaseIntegration):
    BASE_URL = "https://api.modrinth.com/v2"
    integration_type = IntegrationType.modrinth

    async def get_content(self, content: TypedContent) -> CompiledContent:
        url = self.BASE_URL + f"/project/{content.project}/version/{content.version}"

        async with aiohttp.ClientSession() as session, session.get(url) as response:
            if response.status != 200:
                raise Exception(f"{self.__repr__()} is not reachable")
            data = await response.json()
            for file in data.get("files", []):
                if file["primary"]:
                    return CompiledContent(file=file.get("filename"), url=file.get("url"))


async def get_modrinth_integration(
    mod_content_cache_service: ModContentCacheService = Depends(get_mod_cache_service),
    resourcepack_content_cache_service: ResourcepackContentCacheService = Depends(
        get_resourcepack_content_cache_service
    ),
) -> ModrinthIntegration:
    cache_services: list[CacheService] = [
        mod_content_cache_service,
        resourcepack_content_cache_service,
    ]
    return ModrinthIntegration(cache_services)
