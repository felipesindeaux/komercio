from django.urls import path

from users.views import ListCreateUserView, ListNewestUserView, LoginView, UpdateUserStatusView, UpdateUserView

urlpatterns = [
    path('accounts/', ListCreateUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('accounts/newest/<int:num>/', ListNewestUserView.as_view()),
    path('accounts/<pk>/', UpdateUserView.as_view()),
    path('accounts/<pk>/management/', UpdateUserStatusView.as_view())
]
