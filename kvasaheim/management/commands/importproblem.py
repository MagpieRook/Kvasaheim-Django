from django.core.management.base import BaseCommand, CommandError
from kvasaheim.models import Category, Problem

class Command(BaseCommand):
    help = 'Creates a problem from the specified path'

def add_arguments(self, parser):
    parser.add_argument('problem', nargs='+', type=str)

    parser.add_argument(
        '--replace',
        action='store_true',
        dest='replace',
        help='Delete and replace any conflicting problem',
    )

def handle(self, *args, **options):
    for problemfile in options['problem']:
        try:
            # from https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
            import importlib.util
            spec = importlib.util.spec_from_file_location("")
        except User.DoesNotExist:
            raise CommandError('User "%s" does not exist' % username)

        if options['delete']:
            if user.is_superuser:
                user.delete()
                self.stdout.write(self.style.SUCCESS('Succesfully deleted superuser "%s"' % username))
            else:
                raise CommandError('User "%s" is not a superuser' % username)
        else:
            user.is_superuser = True
            user.is_staff = True
            user.is_admin = True
            user.save()

            self.stdout.write(self.style.SUCCESS('Successfully made user "%s" superuser' % username))