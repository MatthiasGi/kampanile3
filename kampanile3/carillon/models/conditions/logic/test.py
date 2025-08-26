from datetime import datetime

from django.test import TestCase

from .. import build_condition


class ConditionTestCase(TestCase):
    def test_build_not_condition(self):
        data = {
            "type": "not",
            "condition": {
                "type": "minute",
                "minute": "20",
            },
        }
        self.assertTrue(build_condition(data).is_valid)
        data["condition"]["type"] = "invalid"
        self.assertFalse(build_condition(data).is_valid)

    def test_not_condition_is_met(self):
        data = {
            "type": "not",
            "condition": {
                "type": "minute",
                "minute": datetime.now().minute,
            },
        }
        self.assertFalse(build_condition(data).is_met)
        data["condition"]["minute"] = (datetime.now().minute + 1) % 60
        self.assertTrue(build_condition(data).is_met)

    def test_and_condition_is_met(self):
        data = {
            "type": "and",
            "conditions": [
                {"type": "minute", "minute": datetime.now().minute},
                {
                    "type": "time",
                    "hour": datetime.now().hour,
                    "minute": datetime.now().minute,
                    "comparator": "gte",
                },
            ],
        }
        self.assertTrue(build_condition(data).is_met)
        data["conditions"][0]["minute"] = (datetime.now().minute + 1) % 60
        self.assertFalse(build_condition(data).is_met)

    def test_or_condition_is_met(self):
        data = {
            "type": "or",
            "conditions": [
                {"type": "minute", "minute": datetime.now().minute},
                {
                    "type": "time",
                    "hour": datetime.now().hour,
                    "minute": datetime.now().minute,
                    "comparator": "gte",
                },
            ],
        }
        self.assertTrue(build_condition(data).is_met)
        data["conditions"][0]["minute"] = (datetime.now().minute + 1) % 60
        self.assertTrue(build_condition(data).is_met)
        data["conditions"][1]["comparator"] = "lt"
        self.assertFalse(build_condition(data).is_met)
