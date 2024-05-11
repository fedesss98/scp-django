from django.core.management.base import BaseCommand
from django.db.models import Count
from events.models import Race


class Command(BaseCommand):
    help = 'Delete duplicate Race instances'

    def handle(self, *args, **options):
        # Group Race instances by 'event' and 'number' fields and annotate each group with the count of instances
        duplicates = (Race.objects.values('event', 'number')
                      .annotate(count=Count('id'))
                      .filter(count__gt=1))

        print(f"There are {len(duplicates)} duplicates to remove")

        for duplicate in duplicates:
            # Get all Race instances in the group except one
            to_delete = (Race.objects.filter(event=duplicate['event'], number=duplicate['number'])
                         .exclude(id=Race.objects.filter(event=duplicate['event'], number=duplicate['number'])
                         .order_by('id')[0].id))
            # Delete the Race instances
            to_delete.delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted duplicate Race instances'))