from django.urls import path
from . import views

app_name = 'work'

urlpatterns = [
    path(
        '',
        views.CompList.as_view(),
        name='comp_list'
    ),
    path(
        'companies/<int:pk>/',
        views.CompDetail.as_view(),
        name='comp_detail'
    ),
    path(
        'companies/<int:pk>/managers/',
        views.ManagList.as_view(),
        name='manag_list'
    ),
    path(
        'workers/',
        views.WorkerList.as_view(),
        name='worker_list'
    ),
    path(
        'workers/<int:pk>/',
        views.WorkerDetail.as_view(),
        name='worker_detail'
    ),
    path(
        'new_work',
    ),
    path(
        'hire',
    ),
]