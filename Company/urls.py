from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import createCompany

app_name = 'company'

urlpatterns = [
    path('createCompany', createCompany.as_view(), name='user_register'),
    #    path('login', LoginUserView.as_view(), name='user_login'),
    #    path('<int:pk>', getAccountInfoview.as_view(), name='account_info'),
    #    path('getAccounts', getAllAccountInfoview.as_view(), name='accounts_info'),
    #    path('logout', logoutAccountView.as_view(), name='accounts_info'),
]
