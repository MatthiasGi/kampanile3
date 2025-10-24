import mido
from django.test import TestCase
from django.test.utils import skipUnless

from .models import Carillon, Rule, Striker


def _check_mido_port():
    try:
        port = mido.open_output()
        port.close()
        return True
    finally:
        return False


class ModelsTestCase(TestCase):
    @skipUnless(_check_mido_port(), "MIDO output port not available")
    def test_rule_validation(self):
        data = {"type": "minute", "minute": 30}
        carillon = Carillon.objects.create(name="Test Carillon")
        striker = Striker.objects.create(name="Test Striker", carillon=carillon)
        rule = Rule.objects.create(name="Test Rule", condition=data, striker=striker)
        rule.condition = {"type": "invalid"}
        self.assertRaises(ValueError, rule.full_clean)
