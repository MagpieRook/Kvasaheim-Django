from django.urls import include, path
from . import views

app_name = 'samplestatistics'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.problem_detail, name='problem_detail'),
    path('<int:pk>/answer/', views.problem_answer, name='problem_answer'),
]