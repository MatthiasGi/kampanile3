from datetime import date, datetime

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
        self.assertTrue(build_condition(data).is_valid)
        for param in ["hour", "minute", "comparator"]:
            errouneous = data.copy()
            errouneous.pop(param)
            self.assertFalse(build_condition(errouneous).is_valid)
        errouneous = data.copy()
        errouneous["comparator"] = "test"
        self.assertFalse(build_condition(errouneous).is_valid)
        errouneous["comparator"] = "gt"
        errouneous["hour"] = 24
        self.assertFalse(build_condition(errouneous).is_valid)
        errouneous["hour"] = 23
        errouneous["minute"] = 60
        self.assertFalse(build_condition(errouneous).is_valid)

    def test_time_condition_is_met(self):
        now = datetime.now()
        data = {
            "type": "time",
            "hour": now.hour,
            "minute": now.minute,
            "comparator": "gt",
        }
        condition = build_condition(data)
        self.assertFalse(condition.is_met)
        data["comparator"] = "lt"
        condition = build_condition(data)
        self.assertFalse(condition.is_met)
        data["comparator"] = "gte"
        condition = build_condition(data)
        self.assertTrue(condition.is_met)
        data["comparator"] = "lte"
        condition = build_condition(data)
        self.assertTrue(condition.is_met)

    def test_build_minute_condition(self):
        data = {"type": "minute"}
        self.assertFalse(build_condition(data).is_valid)
        data["minute"] = datetime.now().minute
        self.assertTrue(build_condition(data).is_valid)

    def test_minute_condition_is_met(self):
        minute = datetime.now().minute
        data = {"type": "minute", "minute": minute}
        condition = build_condition(data)
        self.assertTrue(condition.is_met)
        data["minute"] = (minute + 1) % 60
        condition = build_condition(data)
        self.assertFalse(condition.is_met)

    def test_modulo_minute_condition_is_met(self):
        minute = datetime.now().minute
        data = {"type": "minute_modulo", "modulo": 5, "remainder": minute % 5}
        condition = build_condition(data)
        self.assertTrue(condition.is_met)
        data["remainder"] = (minute + 1) % 5
        condition = build_condition(data)
        self.assertFalse(condition.is_met)

    def test_build_minute_modulo_condition(self):
        data = {"type": "minute_modulo"}
        self.assertFalse(build_condition(data).is_valid)
        data["modulo"] = 5
        self.assertFalse(build_condition(data).is_valid)
        data["remainder"] = 0
        self.assertTrue(build_condition(data).is_valid)
        data["modulo"] = -1
        self.assertFalse(build_condition(data).is_valid)
        data["modulo"] = 0
        self.assertFalse(build_condition(data).is_valid)
        data["modulo"] = "a"
        self.assertFalse(build_condition(data).is_valid)
        data["modulo"] = 5
        data["remainder"] = -1
        self.assertFalse(build_condition(data).is_valid)
        data["remainder"] = 60
        self.assertFalse(build_condition(data).is_valid)
        data["remainder"] = "a"
        self.assertFalse(build_condition(data).is_valid)

    def test_modulo_hour_condition_is_met(self):
        hour = datetime.now().hour
        data = {"type": "hour_modulo", "modulo": 5, "remainder": hour % 5}
        condition = build_condition(data)
        self.assertTrue(condition.is_met)
        data["remainder"] = (hour + 1) % 5
        condition = build_condition(data)
        self.assertFalse(condition.is_met)

    def test_build_hour_modulo_condition(self):
        data = {"type": "hour_modulo"}
        self.assertFalse(build_condition(data).is_valid)
        data["modulo"] = 5
        self.assertFalse(build_condition(data).is_valid)
        data["remainder"] = 0
        self.assertTrue(build_condition(data).is_valid)
        data["modulo"] = -1
        self.assertFalse(build_condition(data).is_valid)
        data["modulo"] = 0
        self.assertFalse(build_condition(data).is_valid)
        data["modulo"] = "a"
        self.assertFalse(build_condition(data).is_valid)
        data["modulo"] = 5
        data["remainder"] = -1
        self.assertFalse(build_condition(data).is_valid)
        data["remainder"] = 24
        self.assertFalse(build_condition(data).is_valid)
        data["remainder"] = "a"
        self.assertFalse(build_condition(data).is_valid)

    def test_build_date_condition(self):
        data = {"type": "date", "comparator": "eq"}
        self.assertFalse(build_condition(data).is_valid)
        data["day"] = 1
        self.assertFalse(build_condition(data).is_valid)
        data["month"] = 1
        self.assertTrue(build_condition(data).is_valid)
        data["day"] = 32
        self.assertFalse(build_condition(data).is_valid)
        data["day"] = 0
        self.assertFalse(build_condition(data).is_valid)
        data["day"] = "a"
        self.assertFalse(build_condition(data).is_valid)
        data["day"] = 1
        data["month"] = 13
        self.assertFalse(build_condition(data).is_valid)
        data["month"] = 0
        self.assertFalse(build_condition(data).is_valid)
        data["month"] = "a"
        self.assertFalse(build_condition(data).is_valid)

    def test_date_condition_is_met(self):
        today = date.today()
        data = {
            "type": "date",
            "day": today.day,
            "month": today.month,
            "comparator": "eq",
        }
        condition = build_condition(data)
        self.assertTrue(condition.is_met)
        data["comparator"] = "gt"
        condition = build_condition(data)
        self.assertFalse(condition.is_met)
        data["comparator"] = "lt"
        condition = build_condition(data)
        self.assertFalse(condition.is_met)
        data["comparator"] = "gte"
        condition = build_condition(data)
        self.assertTrue(condition.is_met)
        data["comparator"] = "lte"
        condition = build_condition(data)
        self.assertTrue(condition.is_met)

    def test_weekday_condition_is_met(self):
        today = date.today()
        data = {"type": "weekday", "weekday": today.weekday()}
        condition = build_condition(data)
        self.assertTrue(condition.is_met)
        data["weekday"] = (today.weekday() + 1) % 7
        condition = build_condition(data)
        self.assertFalse(condition.is_met)

        weekdays = [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ]
        for i, weekday in enumerate(weekdays):
            data["weekday"] = weekday
            condition = build_condition(data)
            if today.weekday() == i:
                self.assertTrue(condition.is_met)
            else:
                self.assertFalse(condition.is_met)
