from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
	help = 'Makes the specified Google User a superuser'

	def add_arguments(self, parser):
		parser.add_argument('user', nargs='+', type=str)

		parser.add_argument(
			'--delete',
			action='store_true',
			dest='delete',
			help='Delete superuser',
		)

	def handle(self, *args, **options):
		for username in options['user']:
			try:
				user = User.objects.get(username=username)
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