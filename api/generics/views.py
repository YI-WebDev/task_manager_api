from typing import ClassVar
from rest_framework import viewsets
from ninja import NinjaAPI
from ninja.router import Router

api = NinjaAPI()
router = Router()

class AsyncNinjaViewSet:
    view_is_async: ClassVar[bool] = True
    
    async def dispatch(self, request, *args, **kwargs):
        return await super().dispatch(request, *args, **kwargs)

class BaseGenericViewSet(AsyncNinjaViewSet, viewsets.GenericViewSet):
    """
    Base ViewSet for partial CRUD operations
    """
    lookup_field = 'hash_id'

    async def perform_destroy(self, instance):
        await instance.soft_delete()

class BaseModelViewSet(BaseGenericViewSet):
    """
    Base ViewSet that provides all CRUD operations
    """
    pass
