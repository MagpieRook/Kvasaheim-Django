from django.urls import include, path
from . import views

app_name = 'kvasaheim'
urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:title>', views.home, name='home'),
    path('category/<int:cpk>/', views.home, name='home'),
    path('realm/<int:rpk>/category/<int:cpk>/', views.home, name='home'),
    path('problem/<int:pk>/', views.problem_detail, name='problem_detail'),
    path('problem/<int:pk>/<int:ipk>/', views.problem_detail, name='problem_detail'),
    path('problem/<int:pk>/answer/<int:apk>/', views.problem_answer, name='problem_answer'),
    path('user/<str:user>/', views.user_profile, name='user_profile')
]