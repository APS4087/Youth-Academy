from django.urls import path, include
from . import views

urlpatterns = [
    
    path('', views.land_page, name='land_page'),
    
    path('login_page/', views.login_page, name='login_page'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register_user, name = 'register'),
    path('staff_list/', views.staff_list_page, name = 'staff_list'),
    path('stu_list/', views.stu_list_page, name = 'stu_list'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('<int:id>', views.view_staff, name='view_staff'),
]
