from django.urls import path
from . import views


urlpatterns = [
  path('all/', views.all_products, name='all-products'),
  path('create/', views.create_product, name='create-product'),
  path('<str:pk>/', views.get_product, name='single-product'),
  path('<str:pk>/update/', views.update_product, name='update-product'),
  path('<str:pk>/delete/', views.delete_product, name='delete-product'),

  path('<str:pk>/reviews/create/', views.create_review, name='create-review'),
  path('<str:pk>/reviews/delete/', views.delete_review, name='delete-review'),
]