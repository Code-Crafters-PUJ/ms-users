from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterRootAccountView, updateRootAccountView, temporalpasswordView, changePasswordAccountView, UpdatePlanView, contactUsView, ServicesView, ServicesTypeView, PlansView, CouponView, TrialsCompanyView, BillsView, TrialsView, RegisterAccountView, LoginUserView, getAccountInfoview, allUsersInfobyCompany, logoutAccountView, getRootAccount, deleteAccountView
app_name = 'user'

urlpatterns = [
    path('register', RegisterRootAccountView.as_view(), name='user_register'),
    path('createUser', RegisterAccountView.as_view(), name='user_register'),
    path('updatePlan/<int:pk>', UpdatePlanView.as_view(), name='update_plan'),
    path('actualPlans', BillsView.as_view(), name='update_plan'),
    path('actualTrials', TrialsView.as_view(), name='update_plan'),
    path('getTrialsCompany', TrialsCompanyView.as_view(), name='update_plan'),
    path('plans', PlansView.as_view(), name='update_plan'),
    path('services/<int:pk>', ServicesTypeView.as_view(), name='update_plan'),
    path('isCouponAvailable/<int:pk>', CouponView.as_view(), name='update_plan'),
    path('services/<int:pk>', ServicesView.as_view(), name='update_plan'),
    path('login', LoginUserView.as_view(), name='user_login'),
    path('<int:pk>', getAccountInfoview.as_view(), name='account_info'),
    path('getAccountsByCompany/<int:pk>',
         allUsersInfobyCompany.as_view(), name='accounts_info'),
    path('changePassword/<int:pk>',
         changePasswordAccountView.as_view(), name='accounts_info'),
    path('updateRootUser',
         updateRootAccountView.as_view(), name='accounts_info'),
    path('getRootAccount/<int:pk>', getRootAccount.as_view(), name='company_info'),
    path('logout', logoutAccountView.as_view(), name='accounts_info'),
    path('contactUs', contactUsView.as_view(), name='accounts_delete'),
    path('temporalpassword', temporalpasswordView.as_view(), name='accounts_delete'),
    path('deleteUser/<int:idUser>/<int:idCompany>', deleteAccountView.as_view(), name='accounts_delete')
]
