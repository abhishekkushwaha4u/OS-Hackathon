from django.urls import path
from . import views
urlpatterns = [
    path('user/', views.CreateUser.as_view()),
    path('confirm/', views.OTPVerify.as_view()),
    path('notifications/', views.UserCategoryNotification.as_view()),
    path('login/', views.Login.as_view()),
    path('clear/', views.ClearDb.as_view()),
    path('manualcreate/', views.CreateUserCategoriesMessageSender.as_view()),
    path('message/records/', views.MessagesUploadedByUser.as_view()),
]
