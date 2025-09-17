from django.db import IntegrityError
from django.test import TestCase

from .models import Input


class InputTestCase(TestCase):
    def test_unique_pin(self):
        Input.objects.create(name="Input 1", pin="D1", active=True)
        # Inactive inputs can share pins
        Input.objects.create(name="Input 2", pin="D1", active=False)
        # Active inputs can share pins if one is empty
        Input.objects.create(name="Input 3", pin="", active=True)
        Input.objects.create(name="Input 4", pin="", active=True)
        # Active inputs cannot share pins
        self.assertRaises(
            IntegrityError, Input.objects.create, name="Input 5", pin="D1", active=True
        )
