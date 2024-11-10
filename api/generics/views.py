from adrf.viewsets import ViewSet as ADRFViewSet
from django.utils.functional import classproperty
from rest_framework import viewsets


class AsyncViewSet(ADRFViewSet):
    @classproperty
    def view_is_async(cls) -> bool:
        return True


class BaseGenericViewSet(AsyncViewSet, viewsets.GenericViewSet):
    """
    Base ViewSet for partial CRUD operations
    """
    lookup_field = 'hash_id'

    def perform_destroy(self, instance):
        instance.soft_delete()


class BaseModelViewSet(BaseGenericViewSet):
    """
    Base ViewSet that provides all CRUD operations
    """
    pass