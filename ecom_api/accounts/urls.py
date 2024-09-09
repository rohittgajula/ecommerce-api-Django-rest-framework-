from django.urls import path
from . import views


urlpatterns = [
  path('all-users/', views.all_users, name='all-users'),
  path('register/', views.register, name='register'),
  path('me/',views.current_user, name='current-user'),
  path('me/update/', views.update_user, name='update-user'),
  path('me/delete/', views.delete_user, name='delete-user'),
]