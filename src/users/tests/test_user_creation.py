from django.test import TestCase

from ..services import create_user
from ..models import User


class UserCreateTests(TestCase):
    def test_user_create_service(self):
        create_user(
            email="user1724@test.com",
            password="Test1234",
        )

        self.assertEqual(User.objects.all().count(), 1)
