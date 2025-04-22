from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and auth
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search_items, name='search'),
    
    # Lost items
    path('lost/', views.LostItemListView.as_view(), name='lost-items'),
    path('lost/<int:pk>/', views.LostItemDetailView.as_view(), name='lost-item-detail'),
    path('lost/new/', views.LostItemCreateView.as_view(), name='lost-item-create'),
    path('lost/<int:pk>/update/', views.LostItemUpdateView.as_view(), name='lost-item-update'),
    path('lost/<int:pk>/delete/', views.LostItemDeleteView.as_view(), name='lost-item-delete'),
    path('lost/<int:pk>/toggle-status/', views.toggle_lost_item_status, name='toggle-lost-status'),
    
    # Found items
    path('found/', views.FoundItemListView.as_view(), name='found-items'),
    path('found/<int:pk>/', views.FoundItemDetailView.as_view(), name='found-item-detail'),
    path('found/new/', views.FoundItemCreateView.as_view(), name='found-item-create'),
    path('found/<int:pk>/update/', views.FoundItemUpdateView.as_view(), name='found-item-update'),
    path('found/<int:pk>/delete/', views.FoundItemDeleteView.as_view(), name='found-item-delete'),
    path('found/<int:pk>/toggle-status/', views.toggle_found_item_status, name='toggle-found-status'),
    
    # Claims
    path('claim/<int:pk>/<str:item_type>/', views.claim_item, name='claim-item'),
    path('claim/<int:claim_id>/approve/', views.approve_claim, name='approve-claim'),
]