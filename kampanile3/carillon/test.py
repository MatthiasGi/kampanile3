from django.test import TestCase

from .models import Rule


class ModelsTestCase(TestCase):
    def test_rule_validation(self):
        data = {"type": "minute", "minute": 30}
        rule = Rule.objects.create(name="Test Rule", condition=data)
        rule.condition = {"type": "invalid"}
        self.assertRaises(ValueError, rule.full_clean)
