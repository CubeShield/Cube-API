from abc import ABC, abstractmethod

from app.core.utils import hash_dict
from app.schemas.content_schema import (
    CachedContent,
    CompiledContent,
    ContentType,
    TypedContent,
)
from app.schemas.integration_schema import IntegrationType
from app.services.cache_service import CacheService
from app.services.mod.mod_content_cache_service import ModContentCacheService
from app.services.resourcepack.resourcepack_content_cache_service import (
    ResourcepackContentCacheService,
)


class BaseIntegration(ABC):
    BASE_URL: str
    integration_type: IntegrationType
    service_map = {
        ContentType.mods.name: ModContentCacheService,
        ContentType.resourcepacks.name: ResourcepackContentCacheService,
    }

    def __init__(self, cache_services: list[CacheService]):
        self.cache_services = cache_services

    async def get_cache_service(self, content: TypedContent) -> CacheService | None:
        content_cache_service_class = self.service_map.get(content.content_type.name)
        for cache_service in self.cache_services:
            if isinstance(cache_service, content_cache_service_class):
                return cache_service
        return None

    @abstractmethod
    async def get_content(self, content: TypedContent) -> CompiledContent:
        pass

    async def get_valid_content(self, content: TypedContent) -> CompiledContent:
        cache_service = await self.get_cache_service(content)
        if cache_service:
            cached_content = await cache_service.get_valid_cache(content)
            if cached_content:
                return cached_content
        compiled_content = await self.get_content(content)
        if compiled_content:
            if cache_service:
                await self.cache_content(content, compiled_content, cache_service)
            return compiled_content
        print(f"{content.model_dump()} Failed")

    async def get_contents(self, contents: list[TypedContent]) -> list[CompiledContent]:
        compiled_contents = []

        for content in contents:
            compiled_content = await self.get_valid_content(content)
            if compiled_content:
                compiled_contents.append(compiled_content)

        return compiled_contents

    async def cache_content(
        self,
        content: TypedContent,
        compiled_content: CompiledContent,
        cache_service: CacheService,
    ):
        cached_content = CachedContent(**compiled_content.model_dump(), hash=hash_dict(content.model_dump()))
        await cache_service.add_cache(cached_content)
