import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from subscriptions.models import Service

class Command(BaseCommand):
    help = "Seeds the database with 500 popular and tech-oriented services"

    def handle(self, *args, **options):
        fake = Faker()
        
        # 1. A curated list of highly recognizable real-world tech services for a clean UI
        popular_services = [
            "Netflix", "Spotify", "Amazon Web Services (AWS)", "Google Cloud", "Microsoft Azure",
            "GitHub", "GitLab", "Slack", "Zoom", "Figma", "Canva", "Notion", "Trello", "Asana",
            "Jira", "Linear", "Stripe", "PayPal", "Shopify", "Mailchimp", "SendGrid", "Twilio",
            "Heroku", "Vercel", "Netlify", "DigitalOcean", "Cloudflare", "Datadog", "Sentry",
            "New Relic", "MongoDB Atlas", "Supabase", "Firebase", "Auth0", "Okta", "ChatGPT",
            "Midjourney", "Claude AI", "HubSpot", "Salesforce", "Intercom", "Loom", "Discord"
        ]

        self.stdout.write("Generating 500 unique services...")

        # 2. Extract existing names from DB to guarantee unique constraints are met
        existing_names = set(Service.objects.values_list('name', flat=True))
        
        services_to_create = []

        # Function to generate tech-sounding names for the remaining balance
        def generate_tech_name():
            # Mix a word/syllable with a tech suffix to keep it looking like a modern platform
            prefixes = ["Cloud", "Data", "Byte", "Flow", "Net", "Sync", "Link", "Snap", "Apex", "Nova", "Pulse"]
            suffixes = ["ly", "ify", "io", "AI", "Hub", "Grid", "Lab", "Wave", "Stack", "Zone", "Forge"]
            
            # 30% chance to just use a clean single domain word, 70% to combine
            if random.random() < 0.3:
                return fake.domain_word().capitalize()
            return f"{random.choice(prefixes)}{random.choice(suffixes)}"

        # Loop until we queue exactly 500 unique services
        while len(services_to_create) < 500:
            # Pick from real list first, then switch to programmatic generation
            if popular_services:
                name = popular_services.pop(0)
                is_custom = False
                is_approved = True
            else:
                name = generate_tech_name()
                is_custom = random.choice([True, False])
                # If custom, randomly decide if it's admin-approved yet
                is_approved = True if not is_custom else random.choice([True, False])

            # Ensure strict unique constraint safety
            if name in existing_names:
                continue
                
            existing_names.add(name)

            logo_slug = name.lower().replace(" ", "")
            logo_url = f"https://picsum.photos/seed/{logo_slug}/100/100"
            description = fake.paragraph(nb_sentences=2)

            services_to_create.append(
                Service(
                    name=name,
                    logo_url=logo_url,
                    is_custom=is_custom,
                    is_approved=is_approved,
                    description=description
                )
            )

        # 3. Bulk create everything at lightning speed inside a database transaction
        with transaction.atomic():
            Service.objects.bulk_create(services_to_create)

        self.stdout.write(self.style.SUCCESS("Successfully seeded 500 normalized services!"))