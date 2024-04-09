from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Asset, Method, Action, User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "username", "password"]
		extra_kwargs = {"password": {"write_only": True}}

	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		return user

class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Project
		fields = '__all__'
		# extra_kwargs = {"project_owner": {"read_only": True}}

class AssetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Asset
		fields = '__all__'

class MethodSerializer(serializers.ModelSerializer):
	class Meta:
		model = Method
		fields = '__all__'

class ActionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Action
		fields = '__all__'
