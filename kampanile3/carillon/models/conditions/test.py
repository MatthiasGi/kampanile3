from django.test import TestCase

from . import build_condition


class ConditionTestCase(TestCase):
    def test_build_invalid_type(self):
        self.assertRaises(ValueError, build_condition, {"type": "invalid"})

    def test_empty_condition(self):
        condition = build_condition({})
        self.assertTrue(condition.is_met)
