from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and auth
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search_items, name='search'),
    
    # Lost items
    path('lost/', views.LostItemListView.as_view(), name='lost-items'),
    path('lost/<int:pk>/', views.LostItemDetailView.as_view(), name='lost-item-detail'),
    path('lost/new/', views.LostItemCreateView.as_view(), name='lost-item-create'),
    path('lost/<int:pk>/update/', views.LostItemUpdateView.as_view(), name='lost-item-update'),
    path('lost/<int:pk>/delete/', views.LostItemDeleteView.as_view(), name='lost-item-delete'),
    path('lost/<int:pk>/toggle-status/', views.toggle_lost_item_status, name='toggle-lost-status'),
    
    # Claims
    path('claim/<int:pk>/<str:item_type>/', views.claim_item, name='claim-item'),
    path('approve-claim/<int:claim_id>/', views.approve_claim, name='approve-claim'),
]