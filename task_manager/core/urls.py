from django.urls import path
from task_manager.core.views import main_page

urlpatterns = [
    path('', main_page),
]
