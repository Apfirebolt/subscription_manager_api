from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds the database with 100 dummy custom users"

    def handle(self, *args, **options):
        fake = Faker()
        count = 100
        
        self.stdout.write(f"Starting to seed {count} custom users...")

        # Wrap everything in an atomic transaction so it commits to the DB all at once
        with transaction.atomic():
            for i in range(count):
                first_name = fake.first_name()
                last_name = fake.last_name()
                
                # Create a clean username based on the fake name
                username = f"{first_name.lower()}_{last_name.lower()}_{i}"
                
                # Ensure unique email addresses
                email = fake.unique.email()
                
                # Use your custom manager's create_user method so passwords get properly hashed
                User.objects.create_user(
                    email=email,
                    username=username,
                    firstName=first_name,
                    lastName=last_name,
                    password="password123",  # Default test password for all dummy accounts
                    is_active=True,
                    is_staff=False
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} users with hashed passwords!"))