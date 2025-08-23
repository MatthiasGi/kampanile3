from datetime import datetime

from django.test import TestCase

from .. import build_condition


class ConditionTestCase(TestCase):
    def test_build_invalid_type(self):
        self.assertRaises(ValueError, build_condition, {"type": "invalid"})

    def test_build_time_condition(self):
        data = {
            "type": "time",
            "hour": datetime.now().hour,
            "minute": datetime.now().minute,
            "comparator": "gt",
        }
        self.assertTrue(build_condition(data).is_valid())
        for param in ["hour", "minute", "comparator"]:
            errouneous = data.copy()
            errouneous.pop(param)
            self.assertFalse(build_condition(errouneous).is_valid())
        errouneous = data.copy()
        errouneous["comparator"] = "test"
        self.assertFalse(build_condition(errouneous).is_valid())
        errouneous["comparator"] = "gt"
        errouneous["hour"] = 24
        self.assertFalse(build_condition(errouneous).is_valid())
        errouneous["hour"] = 23
        errouneous["minute"] = 60
        self.assertFalse(build_condition(errouneous).is_valid())

    def test_time_condition_is_met(self):
        now = datetime.now()
        data = {
            "type": "time",
            "hour": now.hour,
            "minute": now.minute,
            "comparator": "gt",
        }
        condition = build_condition(data)
        self.assertFalse(condition.is_met())
        data["comparator"] = "lt"
        condition = build_condition(data)
        self.assertFalse(condition.is_met())
        data["comparator"] = "gte"
        condition = build_condition(data)
        self.assertTrue(condition.is_met())
        data["comparator"] = "lte"
        condition = build_condition(data)
        self.assertTrue(condition.is_met())

    def test_build_minute_condition(self):
        data = {"type": "minute"}
        self.assertFalse(build_condition(data).is_valid())
        data["minute"] = datetime.now().minute
        self.assertTrue(build_condition(data).is_valid())
