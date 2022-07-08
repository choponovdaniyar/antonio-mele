from django.urls import path
from .views import dashboard, EditProfileView, register, user_detail, user_list, user_follow
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', 
        auth_views.LoginView.as_view(), 
        name="login"),
    path('logout/',
        auth_views.LogoutView.as_view(), 
        name="logout"),


    path('password/change/', 
        auth_views.PasswordChangeView.as_view(), 
        name='password_change'),
    path('password/change/done/', 
        auth_views.PasswordChangeDoneView.as_view(), 
        name="password_change_done"),


    path('password/reset/',
        auth_views.PasswordResetView.as_view(),
        name='password/reset'),
    path('password/reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),

    
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('rest/done',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),

    path('', dashboard, name='dashboard'),
    path('register', register, name='register'),
    path('edit/', EditProfileView.as_view(), name='edit'),

    path('users/', user_list, name="user_list"),
    
    path('users/follow/', user_follow, name='user_follow'),
    path('users/<username>/', user_detail, name="user_detail"),
    
]