from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and auth
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='items/logout.html'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search_items, name='search'),
    
    # Lost items
    path('lost/', views.LostItemListView.as_view(), name='lost-items'),
    path('lost/<int:pk>/', views.LostItemDetailView.as_view(), name='lost-item-detail'),
    path('lost/new/', views.LostItemCreateView.as_view(), name='lost-item-create'),
    path('lost/<int:pk>/update/', views.LostItemUpdateView.as_view(), name='lost-item-update'),
    path('lost/<int:pk>/delete/', views.LostItemDeleteView.as_view(), name='lost-item-delete'),
    
    # Found items
    path('found/', views.FoundItemListView.as_view(), name='found-items'),
    path('found/<int:pk>/', views.FoundItemDetailView.as_view(), name='found-item-detail'),
    path('found/new/', views.FoundItemCreateView.as_view(), name='found-item-create'),
    path('found/<int:pk>/update/', views.FoundItemUpdateView.as_view(), name='found-item-update'),
    path('found/<int:pk>/delete/', views.FoundItemDeleteView.as_view(), name='found-item-delete'),
    
    # Claims
    path('claim/<int:pk>/<str:item_type>/', views.claim_item, name='claim-item'),
]