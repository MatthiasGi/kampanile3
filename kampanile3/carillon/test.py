from django.test import TestCase

from .models import Carillon, Rule, Striker


class ModelsTestCase(TestCase):
    def test_rule_validation(self):
        data = {"type": "minute", "minute": 30}
        carillon = Carillon.objects.create(name="Test Carillon")
        striker = Striker.objects.create(name="Test Striker", carillon=carillon)
        rule = Rule.objects.create(name="Test Rule", condition=data, striker=striker)
        rule.condition = {"type": "invalid"}
        self.assertRaises(ValueError, rule.full_clean)
