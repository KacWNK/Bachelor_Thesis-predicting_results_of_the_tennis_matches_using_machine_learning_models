import os
import django

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tennis_bets_site.settings")  # Adjust to your project structure
django.setup()

# Import models after setting up Django
from stats.models import Match

# Delete the object
obj = Match.objects.get(match_id='melbourne_2025_206173_200282')
obj.delete()

print(f"Match with ID 'melbourne_2025_210097_104792' has been deleted.")