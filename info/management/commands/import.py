from django.core.management.base import BaseCommand

import info.importer
from info.models import MasterPage, Page


class Command(BaseCommand):
    help = "Import infopankki site dump into database."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        print('Start of import')
        print('Before import master page count', MasterPage.objects.count())
        print('Before import page count', Page.objects.count())
        info.importer.do_import()
        print('After import master page count', MasterPage.objects.count())
        print('After import page count', Page.objects.count())
