from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ListCustomUserSerializer,
    CustomUserSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    BudgetSerializer,
    ListBudgetSerializer,
    SubscriptionSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import CustomUser
from subscriptions.models import Service, Budget, Subscription
from .serializers import ServiceSerializer, ListServiceSerializer
from .permissions import IsBudgetOwner


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class ListCustomUsersApiView(ListAPIView):
    serializer_class = ListCustomUserSerializer
    queryset = CustomUser.objects.all()


class DetailCustomUserApiView(RetrieveUpdateAPIView):
    serializer_class = ListCustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user = request.user
            # Crucial step: Hash and commit the new password to the database
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response(
                {"detail": "Your security credentials have been updated successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceListCreateAPIView(ListCreateAPIView):
    """
    GET: List all approved services (Public)
    POST: Create a new service (Authenticated users only)
    """

    def get_queryset(self):
        # GET requests only return approved services
        if self.request.method == "GET":
            return Service.objects.all()
        # POST requests use the base queryset context
        return Service.objects.all()

    def get_serializer_class(self):
        # Use the specific read-optimized serializer for listings
        if self.request.method == "GET":
            return ListServiceSerializer
        return ServiceSerializer

    def get_permissions(self):
        # Protect creation endpoint, keep listing completely public
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]


class ServiceDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve service details (Public)
    PUT/PATCH/DELETE: Update or delete a service (Admin only)
    """

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_update(self, serializer):
        # Only allow updates if user is admin or the creator of the service
        service = self.get_object()
        user = self.request.user
        if user.is_staff or (service.is_custom and service.created_by == user):
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to edit this service.")

    def perform_destroy(self, instance):
        # Only allow deletion if user is admin or the creator of the service
        user = self.request.user
        if user.is_staff or (instance.is_custom and instance.created_by == user):
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this service.")


class BudgetListCreateAPIView(ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ListBudgetSerializer
        return BudgetSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BudgetDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated, IsBudgetOwner]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class SubscriptionListCreateAPIView(ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
