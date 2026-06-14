from rest_framework import serializers
from users.models import CustomUser
from subscriptions.models import Service, Budget, Subscription
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': ('No account exists with these credentials, check password and email')
    }

    def validate(self, attrs):
        
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data 
        data.update({'userData': {
            'email': self.user.email,
            'username': self.user.username,
            'id': self.user.id
        }})
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        min_length=8,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'is_staff', 'password', 'access', 'refresh',)
    
    def get_refresh(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh)

    def get_access(self, user):
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token),
        return access

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ListCustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'firstName', 'lastName', 'is_staff',)

    def validate_email(self, value):
        """
        Optional Validation: Ensure that if a user changes their email, 
        it doesn't clash with an existing email address in the database.
        """
        user = self.context['request'].user
        if CustomUser.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return value
    

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Your current password was entered incorrectly.")
        return value

    def validate(self, data):
        validate_password(data['new_password'], user=self.context['request'].user)
        
        if data['current_password'] == data['new_password']:
            raise serializers.ValidationError({"new_password": "The new password cannot be identical to your old one."})
            
        return data


class ServiceSerializer(serializers.ModelSerializer):
               
    class Meta:
        model = Service
        fields = ('name', 'logo_url', 'description',)

    def create(self, validated_data):
        service = super(ServiceSerializer, self).create(validated_data)
        service.save()
        return service

    def validate(self, attrs):
        if attrs['logo_url'] == '':
            raise serializers.ValidationError('Logo URL cannot be blank')
        return attrs
    

class ListServiceSerializer(serializers.ModelSerializer):
               
    class Meta:
        model = Service
        fields = ('id', 'name', 'logo_url', 'description',)


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ('id', 'user', 'amount', 'duration', 'description', 'created_at', 'updated_at', 'is_active')
        read_only_fields = ('id', 'created_at', 'user', 'updated_at')

    def perform_update(self, serializer):
        # if there is no budget active for this user, set this one as active, else set it as inactive
        user = self.context['request'].user
        if not Budget.objects.filter(user=user, is_active=True).exists():
            serializer.save(is_active=True)
        else:
            serializer.save(is_active=False)

    def perform_create(self, serializer):
        # if there is no budget active for this user, set this one as active, else set it as inactive
        user = self.context['request'].user
        if not Budget.objects.filter(user=user, is_active=True).exists():
            serializer.save(user=user, is_active=True)
        else:
            serializer.save(user=self.request.user, is_active=False)


class ListBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ('id', 'amount', 'duration', 'description', 'created_at', 'updated_at', 'is_active')
        read_only_fields = ('id', 'created_at', 'updated_at')



    
class SubscriptionSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')

    class Meta:
        model = Subscription
        fields = (
            'id', 'user', 'service', 'service_name', 'plan_name', 
            'status', 'category', 'cost', 'billing_cycle', 'next_billing_date', 
            'notes', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def validate(self, attrs):
        user = self.context['request'].user

        if not Budget.objects.filter(user=user).exists():
            raise serializers.ValidationError({
                "budget": "You cannot track subscriptions until you establish a target budget threshold. Please configure a budget first."
            })

        return attrs


class ListSubscriptionSerializer(serializers.ModelSerializer):
    service = ListServiceSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ('id', 'service', 'plan_name', 'status', 'cost', 'billing_cycle', 'next_billing_date')