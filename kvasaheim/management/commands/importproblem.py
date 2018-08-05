"""Adds a manage.py command for easy Problem importing."""
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from kvasaheim.models import Category, Path, Problem

class Command(BaseCommand):
    """Adds a Command as per
    https://docs.djangoproject.com/en/2.0/howto/custom-management-commands/"""
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
            # https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
                import importlib.util
                spec = importlib.util.spec_from_file_location("problem", problemfile)
                problem_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(problem_module)
                problemdata = problem_module.Problem
            except AttributeError:
                raise CommandError('%s is not valid file.' % problemfile)

            if options['replace']:
                try:
                    oldproblem = Problem.objects.get(title=problemdata.title)
                    oldproblem.delete()
                except DoesNotExist:
                    self.stdout.write(self.style.NOTICE(
                        '%s is not a model. Ignoring --replace.' % problemdata.title))
            try:
                category = Category.objects.get(title=problemdata.category)
            except DoesNotExist:
                category = Category.objects.create(title=problemdata.category,
                                                   published=problemdata.published)
                category.save()

            try:
                problem = Problem.objects.create(
                    title=problemdata.title,
                    text=problemdata.text,
                    category=category,
                    published=problemdata.published,
                    equation=problemdata.equation,
                    random_low=problemdata.random_low,
                    random_high=problemdata.random_high,
                    num_rands_low=problemdata.num_rands_low,
                    num_rands_high=problemdata.num_rands_high,
                    formula=problemdata.formula,
                    solution=problemdata.solution,
                    rcode=problemdata.rcode,
                    excel=problemdata.excel
                )
                problem.save()
            except IntegrityError:
                raise CommandError('Problem with title %s already exists. ' % problemdata.title +
                                   'Use --replace to delete and replace.')
            except:
                raise CommandError('%s has invalid formatting.' % problemdata.title)
            self.stdout.write(self.style.SUCCESS('Successfully created problem %s' % problem.title))
