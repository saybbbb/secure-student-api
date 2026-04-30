from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User


class Command(BaseCommand):
    help = 'Seed user groups (Admin, Faculty, Student) and create test users'

    def handle(self, *args, **options):
        # Create groups
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        faculty_group, _ = Group.objects.get_or_create(name='Faculty')
        student_group, _ = Group.objects.get_or_create(name='Student')
        self.stdout.write(self.style.SUCCESS('✅ Groups created: Admin, Faculty, Student'))

        # Create test users and assign to groups
        users_config = [
            ('admin_user', 'admin123', admin_group),
            ('faculty_user', 'faculty123', faculty_group),
            ('student_user', 'student123', student_group),
        ]

        for username, password, group in users_config:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f'  Created user: {username} → {group.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'  User already exists: {username}'))

        self.stdout.write(self.style.SUCCESS('✅ Seeding complete!'))
