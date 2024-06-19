"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from accounts import views
from finance import views as finance_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name="base.html"), name="base"),
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("add_budget/", finance_views.AddBudget.as_view(), name="add_budget"),
    path("my_budgets/", finance_views.MyBudgets.as_view(), name="my_budgets"),
    path("delete_budget/<int:pk>", finance_views.DeleteBudget.as_view(), name="delete_budget"),
    path("add_transaction/", finance_views.AddTransaction.as_view(), name="add_transaction"),
    path("transaction_list/", finance_views.TransactionList.as_view(), name="transaction_list"),
    path("delete_transaction/<int:pk>/", finance_views.DeleteTransactionView.as_view(), name="delete_transaction"),
    path("update_transaction/<int:pk>/", finance_views.TransactionUpdate.as_view(), name="update_transaction"),
    path("add_category/", finance_views.AddCategoryView.as_view(), name="add_category"),
    path("category_list/", finance_views.CategoryList.as_view(), name="category_list"),
    path("update_category/<int:pk>/", finance_views.UpdateCategoryView.as_view(), name="update_category"),
    path("delete_category/<int:pk>/", finance_views.DeleteCategoryView.as_view(), name="delete_category"),
    path("profile", finance_views.profile, name="profile"),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
