from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from .serializers import UserSerializer, ProjectSerializer, AssetSerializer, ResultSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Project, Asset, Result
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


class BulkAssetUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        try:
            project = Project.objects.get(
                id=project_id, project_owner=request.user)
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
        return Project.objects.filter(project_owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(project_owner=self.request.user)


class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Asset.objects.filter(project__project_owner=self.request.user)


class ResultViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Result.objects.filter(asset__project__project_owner=self.request.user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
