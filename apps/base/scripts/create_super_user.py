import os
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

load_dotenv()

User = get_user_model()

def run():
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

    if not User.objects.filter(username=username).exists():
        print(f"Criando superusuário {username}...")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print(f"Superusuário {username} já existe.")
