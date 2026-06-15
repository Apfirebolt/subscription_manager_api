from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True, max_length=255)
    username = models.CharField("User Name", unique=True, max_length=255, blank=True, null=True)
    firstName = models.CharField("First Name", max_length=100, blank=True, null=True)
    lastName = models.CharField("Last Name", max_length=100, blank=True, null=True)
    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Staff', default=False)
    # many 2 many self relation
    following = models.ManyToManyField(
        'self',
        through='Follow',  # Points to the intermediate table below
        through_fields=('follower', 'following'),
        symmetrical=False,  # Ensures User A following User B doesn't automatically mean B follows A
        related_name='followers'
    )
    profile_image = models.ImageField("Profile Image", upload_to='profile_image/', blank=True, null=True)
    is_superuser = models.BooleanField('Super User', default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        '''Doc string for meta'''
        verbose_name_plural = "User"


class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser, 
        related_name='following_relations', 
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        CustomUser, 
        related_name='follower_relations', 
        on_delete=models.CASCADE
    )
    is_accepted = models.BooleanField(
        default=False, 
        help_text="False means a pending follow request, True means approved follow"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents a user from sending duplicate follow requests to the same person
        unique_together = ('follower', 'following')

    def __str__(self):
        status = "Accepted" if self.is_accepted else "Pending"
        return f"{self.follower.email} ➔ {self.following.email} ({status})"



