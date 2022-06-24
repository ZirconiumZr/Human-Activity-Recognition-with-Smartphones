from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('models/', views.model, name='model'),
    path('upload/', views.upload, name='upload'),
    path('history/', views.history, name='history'),
    path('detail/<str:audio>/', views.detail, name='detail'),
]