from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet, CategoryViewSet
from accounts.views import register, login_view


def home(request):
    return HttpResponse("Task Manager API is working 🚀")


router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home),

    path('api/auth/register/', register),
    path('api/auth/login/', login_view),

    path('api/', include(router.urls)),
]