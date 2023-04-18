from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('tasks/', views.getTasks, name='notes'),
    path('tasks/<str:pk>', views.getTask, name='note'),
    path('login/', views.loginPage, name='login'),
    path('user-forgot-password/', views.ResetPassword, name='reset_password'),
    path('user-change-password/<str:pk>', views.ChangePassword, name='change_password'),

]
