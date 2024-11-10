from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrentUserView, DownloadSelectedView, LoginView, CreateUserView, DataViewSet, UploadFileToS3View, DownloadAllView, DeleteFileView

router = DefaultRouter()

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('current-user/', CurrentUserView.as_view(), name='current-user'),
    path('', include(router.urls))
]