from django.urls import path
from .views import (
    ListCustomUsersApiView,
    CreateCustomUserApiView,
    DetailCustomUserApiView,
    ServiceListCreateAPIView,
    ServiceDetailAPIView,
    BudgetListCreateAPIView,
    BudgetDetailAPIView,
    SubscriptionListCreateAPIView,
    SubscriptionDetailAPIView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register", CreateCustomUserApiView.as_view(), name="signup"),
    path("login", TokenObtainPairView.as_view(), name="signin"),
    path("refresh", TokenRefreshView.as_view(), name="refresh"),
    path("profile", DetailCustomUserApiView.as_view(), name="me"),
    path("users", ListCustomUsersApiView.as_view(), name="list-users"),
    path("services", ServiceListCreateAPIView.as_view(), name="services"),
    path("services/<int:pk>", ServiceDetailAPIView.as_view(), name="service-detail"),
    path("budgets", BudgetListCreateAPIView.as_view(), name="budgets"),
    path("budgets/<int:pk>", BudgetDetailAPIView.as_view(), name="budget-detail"),
    path("subscriptions", SubscriptionListCreateAPIView.as_view(), name="subscriptions"),
    path("subscriptions/<int:pk>", SubscriptionDetailAPIView.as_view(), name="subscription-detail"),
]
