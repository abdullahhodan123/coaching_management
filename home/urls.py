from django.urls import path
from . import views

urlpatterns = [
    path('',               views.home_view,     name='home'),
    path('notice/add/',    views.notice_add,    name='notice_add'),
    path('notice/<int:pk>/edit/',   views.notice_edit,   name='notice_edit'),
    path('notice/<int:pk>/delete/', views.notice_delete, name='notice_delete'),
]