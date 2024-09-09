from django.urls import path
from . import views


urlpatterns = [
  path('all/', views.all_orders, name='all-orders'),
  path('<str:pk>/', views.get_order, name='get-order'),
  path('new_order/', views.new_order, name='new-order'),
  path('<str:pk>/delete/', views.delete_order, name='delate-order'),
]

