from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', views.UsersViewSet, basename='users')

urlpatterns = [
    path(r'', include(router.urls)),
]
