from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:company_id>/', views.detail, name='detail'),
]

# app_name = 'work'
# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),
#     path('<int:pk>/', views.DetailView.as_view(), name='detail'),
# ]