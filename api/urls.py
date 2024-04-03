from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, AssetViewSet, ResultViewSet, BulkAssetUploadView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'assets', AssetViewSet, basename='asset')
router.register(r'results', ResultViewSet, basename='result')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('projects/<int:project_id>/bulk-upload/',
         BulkAssetUploadView.as_view(), name='bulk-asset-upload'),
]
