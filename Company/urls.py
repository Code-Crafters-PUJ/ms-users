from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import createCompany, getInfoCompany, validBranchView, getInfoPlanCompany

app_name = 'company'

urlpatterns = [
    path('createCompany', createCompany.as_view(), name='company_register'),
    path('<int:pk>', getInfoCompany.as_view(), name='company_info'),
    path('edit', getInfoCompany.as_view(), name='company_info'),
    path('modules/<int:pk>', getInfoCompany.as_view(), name='company_info'),
    path('actualPlan/<int:pk>', getInfoPlanCompany.as_view(), name='company_info'),
    path('valid/branchId/<int:pk>', validBranchView.as_view(), name='company_info'),
    #    path('<int:pk>', getAccountInfoview.as_view(), name='account_info'),
    #    path('getAccounts', getAllAccountInfoview.as_view(), name='accounts_info'),
    #    path('logout', logoutAccountView.as_view(), name='accounts_info'),
]
