from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('articles/', views.article_list, name='article_list'),
    path('mrp/', views.mrp_view, name='mrp_view'),
    path('capacity/', views.capacity_view, name='capacity_view'),
    path('decalages/', views.offset_graph_view, name='offset_graph_view'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/new/', views.order_create, name='order_create'),
    path('orders/<int:pk>/confirm/', views.order_confirm, name='order_confirm'),
    path('generate-of/', views.generate_of, name='generate_of'),
    path('manufacturing/', views.mo_list, name='mo_list'),
    path('workorders/<int:pk>/<str:status>/', views.workorder_status, name='workorder_status'),
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/new/', views.maintenance_create, name='maintenance_create'),
]
