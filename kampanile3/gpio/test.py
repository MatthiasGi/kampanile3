from django.db import IntegrityError
from django.test import TestCase
from django.test.utils import skipIf

from .models import Input


def _check_inputs():
    import microcontroller

    if microcontroller.chip_id is None:
        return False

    from .forms import get_board_pins

    return sum(1 for _ in get_board_pins()) > 1


class InputTestCase(TestCase):
    @skipIf(_check_inputs, "No board detected")
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
