from django.urls import path
from . import views


urlpatterns = [
    path('interface/', views.interface, name='interface'),
    path('interface/<int:inter_id>/', views.interfaceDetail, name='interface-detail'),
    
    path('create-interface/', views.createInterface, name='create-interface'),
    path('edit-interface/<int:interface_id>/', views.updateInterface, name='update-interface'),
]