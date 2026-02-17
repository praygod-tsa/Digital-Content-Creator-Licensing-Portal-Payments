from datetime import date

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from applicants.models import Applicant, Application, FeeSchedule


class Command(BaseCommand):
    help = 'Create default staff role groups and seed basic FeeSchedule rows for pilot use.'

    def handle(self, *args, **options):
        role_names = [
            'ROLE_TCRA_REVIEWER',
            'ROLE_MINISTRY_FUND_REVIEWER',
            'ROLE_MINISTRY_LEADERSHIP_READONLY',
        ]

        for role_name in role_names:
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group.name}'))
            else:
                self.stdout.write(f'Group already exists: {group.name}')

        effective_from = date(2025, 1, 1)
        example_rows = [
            # Amateur
            (Applicant.CreatorType.AMATEUR, True, 5_000),
            # Professional creator
            (Applicant.CreatorType.PROFESSIONAL, False, 50_000),
            # Aggregator
            (Applicant.CreatorType.AGGREGATOR, False, 100_000),
        ]

        created_count = 0
        for licence_category, _label in Application.LicenceCategory.choices:
            for creator_type, is_amateur, amount in example_rows:
                _, created = FeeSchedule.objects.get_or_create(
                    licence_category=licence_category,
                    creator_type=creator_type,
                    is_amateur=is_amateur,
                    fee_type=FeeSchedule.FeeType.APPLICATION,
                    effective_from=effective_from,
                    defaults={
                        'amount_tzs': amount,
                        'is_active': True,
                        'effective_to': None,
                    },
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Fee rows created: {created_count}'))
        self.stdout.write(self.style.SUCCESS('Setup completed.'))
