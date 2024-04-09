from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, AssetViewSet, BulkAssetUploadView, ActionViewSet, MethodViewSet, ApplyMethodView

router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='project')
router.register(r'asset', AssetViewSet, basename='asset')
router.register(r'action', ActionViewSet, basename='action')
router.register(r'method', MethodViewSet, basename='method')

urlpatterns = [
	path('', include(router.urls)),
]

urlpatterns += [
	path('projects/<int:project_id>/bulk-upload/',
		BulkAssetUploadView.as_view(), name='bulk-asset-upload'
	),
  path('assets/<int:asset_id>/apply-method/',
		ApplyMethodView.as_view(), name='apply-method'
	),
]