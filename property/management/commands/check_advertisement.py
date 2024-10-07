from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from property.models import Property

class Command(BaseCommand):
    help = 'Check and update advertisement status for properties if the advertisement period has expired.'

    def handle(self, *args, **kwargs):
        timeout_period = timedelta( hours=0.25)  # Advertisement timeout period
        now = timezone.now()

        # Find all properties where is_advertised is True
        properties = Property.objects.filter(is_advertised=True)

        for prop in properties:
            # If the property has been advertised for more than the timeout period, stop advertisement
            if prop.advertised_at and now > (prop.advertised_at + timeout_period):
                prop.stop_advertisement()  # Disable advertisement
                self.stdout.write(self.style.SUCCESS(f'Advertisement stopped for property: {prop.title}'))
