from django.urls import path
from limitedTimeDeal import views

urlpatterns = [
    path('createUser', views.UserProfileApiView.as_view()),
    path('createDeal', views.DealApiView.as_view()),
    path('updateDeal/<str:deal_id>/', views.UpdateDeal.as_view()),
    path('endDeal/<str:deal_id>/', views.EndDeal.as_view()),
    path('claimDeal/<str:deal_id>/', views.ClaimDealApiView.as_view()),
    
]