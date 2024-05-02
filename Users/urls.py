from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterRootAccountView, RegisterAccountView, LoginUserView, getAccountInfoview, allUsersInfobyCompany, logoutAccountView
app_name = 'user'

urlpatterns = [
    path('createRootUser', RegisterRootAccountView.as_view(), name='user_register'),
    path('createUser', RegisterAccountView.as_view(), name='user_register'),
    path('login', LoginUserView.as_view(), name='user_login'),
    path('<int:pk>', getAccountInfoview.as_view(), name='account_info'),
    path('getAccountsByCompany/<int:pk>',
         allUsersInfobyCompany.as_view(), name='accounts_info'),
    path('logout', logoutAccountView.as_view(), name='accounts_info'),
]
