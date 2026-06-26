from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']
        read_only_fields = ['id']


class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )

    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'owner',
            'category',
            'category_id',
            'status',
            'priority',
            'due_date',
            'is_overdue',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                'Title cannot be blank or whitespace.'
            )
        return value.strip()


class TaskListSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(
        source='owner.username',
        read_only=True
    )

    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'status',
            'priority',
            'due_date',
            'is_overdue',
            'owner_name',
            'category_name',
            'created_at',
        ]