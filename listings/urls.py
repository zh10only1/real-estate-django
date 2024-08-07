from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('search', views.search, name='search'),

    path('create-list/', views.createList, name='create-list'),
    path('edit-list/<int:list_id>/', views.updateList, name='update-list'),
]