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
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import CustomUser, Follow
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
        user = self.request.user
        current_budget = self.get_object()
        
        # Check if 'is_active' is being updated in this request
        is_active_input = serializer.validated_data.get('is_active')

        # 1. If trying to deactivate, check if it's the only budget that exists
        if is_active_input is False:
            total_budgets = Budget.objects.filter(user=user).count()
            if total_budgets <= 1:
                raise serializers.ValidationError(
                    {'is_active': 'You cannot deactivate the only budget that exists.'}
                )
                
            # Optional: If you also want to prevent deactivating if no OTHER budget is active
            other_active_exists = Budget.objects.filter(user=user, is_active=True).exclude(pk=current_budget.pk).exists()
            if not other_active_exists:
                raise serializers.ValidationError(
                    {'is_active': 'At least one budget must remain active. Activate another budget first.'}
                )

        # 2. If this budget is being set to active, deactivate ALL OTHER budgets for this user
        if is_active_input is True:
            Budget.objects.filter(user=user).exclude(pk=current_budget.pk).update(is_active=False)
        
        # 3. Save the current budget changes
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


class FollowUserAPIView(APIView):
    """
    POST: Send a follow request to a target user.
    If already requested, returns a 400.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={
            201: inline_serializer(
                name='FollowSuccessResponse',
                fields={'detail': serializers.CharField()}
            ),
            400: inline_serializer(
                name='FollowErrorResponse',
                fields={'detail': serializers.CharField()}
            ),
            404: inline_serializer(
                name='FollowUserNotFoundResponse',
                fields={'detail': serializers.CharField()}
            )
        }
    )
    def post(self, request, user_id, *args, **kwargs):
        follower = request.user
        
        try:
            target_user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if follower == target_user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a relationship already exists
        follow_relation, created = Follow.objects.get_or_create(
            follower=follower, 
            following=target_user
        )

        if not created:
            if follow_relation.is_accepted:
                return Response({"detail": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Follow request is already pending."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Follow request sent successfully."}, status=status.HTTP_201_CREATED)
    

class UnfollowUserAPIView(APIView):
    """
    DELETE: Unfollow a user or cancel a pending follow request.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: inline_serializer(
                name='UnfollowSuccessResponse',
                fields={'detail': serializers.CharField()}
            ),
            400: inline_serializer(
                name='UnfollowErrorResponse',
                fields={'detail': serializers.CharField()}
            ),
            404: inline_serializer(
                name='UnfollowUserNotFoundResponse',
                fields={'detail': serializers.CharField()}
            )
        }
    )
    def delete(self, request, user_id, *args, **kwargs):
        follower = request.user
        
        try:
            target_user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        follow_relation = Follow.objects.filter(follower=follower, following=target_user)

        if follow_relation.exists():
            follow_relation.delete()
            return Response({"detail": "Successfully unfollowed user / canceled request."}, status=status.HTTP_200_OK)
        
        return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
    

class AcceptFollowRequestAPIView(APIView):
    """
    POST: Accept an incoming pending follow request from another user.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={
            200: inline_serializer(
                name='AcceptFollowResponse',
                fields={
                    'detail': serializers.CharField(),
                    'mutual': serializers.BooleanField(required=False)
                }
            ),
            400: inline_serializer(
                name='AcceptFollowErrorResponse',
                fields={'detail': serializers.CharField()}
            ),
            404: inline_serializer(
                name='AcceptFollowNotFoundResponse',
                fields={'detail': serializers.CharField()}
            )
        }
    )
    def post(self, request, user_id, *args, **kwargs):
        current_user = request.user  # The one who received the request (following)
        
        try:
            requester_user = CustomUser.objects.get(id=user_id)  # The one who sent it (follower)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            follow_relation = Follow.objects.get(follower=requester_user, following=current_user)
        except Follow.DoesNotExist:
            return Response({"detail": "No pending follow request found from this user."}, status=status.HTTP_404_NOT_FOUND)

        if follow_relation.is_accepted:
            return Response({"detail": "You have already accepted this follow request."}, status=status.HTTP_400_BAD_REQUEST)

        # Accept the request
        follow_relation.is_accepted = True
        follow_relation.save()

        # Check if it results in a mutual connection to tailor your response message
        is_mutual = current_user.is_mutual_with(requester_user)
        response_data = {"detail": "Follow request accepted."}
        if is_mutual:
            response_data["mutual"] = True
            response_data["detail"] += " You are now mutual followers, unlocking profile features!"

        return Response(response_data, status=status.HTTP_200_OK)
