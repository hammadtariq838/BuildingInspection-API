from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from .serializers import UserSerializer, ProjectSerializer, AssetSerializer, ActionSerializer, MethodSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Project, Asset, Method, Action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


class BulkAssetUploadView(APIView):
	parser_classes = [MultiPartParser, FormParser]
	permission_classes = [IsAuthenticated]

	def post(self, request, project_id):
		try:
			project = Project.objects.get(
					id=project_id, user=request.user)
		except Project.DoesNotExist:
			return Response({'message': 'Project not found or does not belong to you'}, status=status.HTTP_404_NOT_FOUND)

		print('request.FILES:', request.FILES)
		files = request.FILES.getlist('asset_images')
		assets = []

		for file in files:
			asset = Asset(project=project, asset_image=file)
			asset.save()
			assets.append(asset)

		serializer = AssetSerializer(assets, many=True)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectViewSet(viewsets.ModelViewSet):
	serializer_class = ProjectSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Project.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class AssetViewSet(viewsets.ModelViewSet):
	serializer_class = AssetSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Asset.objects.filter(project__user=self.request.user)


class MethodViewSet(viewsets.ModelViewSet):
	serializer_class = MethodSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Method.objects.all()

class ActionViewSet(viewsets.ModelViewSet):
	serializer_class = ActionSerializer
	permission_classes = [IsAuthenticated]

	# get all actions for a specific asset
	def get_queryset(self):
		asset_id = self.kwargs['asset_id']
		if asset_id is not None:
			return Action.objects.filter(asset_id=asset_id)
		else:
	 		return Response({'message': 'Asset ID is required'}, status=status.HTTP_400_BAD_REQUEST)

class CreateUserView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [AllowAny]
