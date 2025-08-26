from datetime import date

from directorium.directorium import Directorium, Season
from directorium.event import Rank
from directorium.utils import easter
from django.test import TestCase

from .. import build_condition


class ConditionTestCase(TestCase):
    def test_build_season_condition(self):
        data = {"type": "season"}
        self.assertFalse(build_condition(data).is_valid)
        data["season"] = "ORDINARY"
        self.assertTrue(build_condition(data).is_valid)
        data["season"] = "invalid"
        self.assertFalse(build_condition(data).is_valid)

    def test_season_condition_is_met(self):
        current_season = Directorium.get_season()
        data = {"type": "season", "season": current_season.name}
        self.assertTrue(build_condition(data).is_met)
        data["season"] = (
            "ORDINARY" if current_season != Season.ORDINARY else "CHRISTMAS"
        )
        self.assertFalse(build_condition(data).is_met)

    def test_build_event_rank_condition(self):
        data = {"type": "event_rank", "comparator": "eq"}
        self.assertFalse(build_condition(data).is_valid)
        data["rank"] = "invalid"
        self.assertFalse(build_condition(data).is_valid)
        data["rank"] = "SOLEMNITY"
        self.assertTrue(build_condition(data).is_valid)
        data["comparator"] = "invalid"
        self.assertFalse(build_condition(data).is_valid)
        data = {"type": "event_rank", "rank": "FEAST"}
        self.assertFalse(build_condition(data).is_valid)

    def test_event_rank_condition_is_met(self):
        current_rank = Directorium.from_request().get()[0].rank
        data = {"type": "event_rank", "rank": current_rank.name, "comparator": "eq"}
        self.assertTrue(build_condition(data).is_met)
        if current_rank != Rank.NONE:
            data["comparator"] = "gt"
            self.assertFalse(build_condition(data).is_met)
            data["rank"] = "NONE"
            self.assertTrue(build_condition(data).is_met)
        else:
            data["comparator"] = "lt"
            self.assertFalse(build_condition(data).is_met)
            data["rank"] = "SOLEMNITY"
            self.assertTrue(build_condition(data).is_met)

    def test_build_event_title_condition(self):
        data = {"type": "event_title"}
        self.assertFalse(build_condition(data).is_valid)
        data["title"] = "Christmas"
        self.assertTrue(build_condition(data).is_valid)

    def test_event_title_condition_is_met(self):
        current_title = Directorium.from_request().get()[0].title
        data = {"type": "event_title", "title": current_title}
        self.assertTrue(build_condition(data).is_met)
        data["title"] = "Some Nonexistent Title"
        self.assertFalse(build_condition(data).is_met)

    def test_build_easter_offset_condition(self):
        data = {"type": "easter_offset", "comparator": "eq"}
        self.assertFalse(build_condition(data).is_valid)
        data["offset"] = "not_an_integer"
        self.assertFalse(build_condition(data).is_valid)
        data["offset"] = "10"
        self.assertTrue(build_condition(data).is_valid)
        data["offset"] = "-10"
        self.assertTrue(build_condition(data).is_valid)
        data["offset"] = "0"
        self.assertTrue(build_condition(data).is_valid)

    def test_easter_offset_condition_is_met(self):
        today = date.today()
        current_year_easter = easter(today.year)
        offset = (today - current_year_easter).days
        data = {"type": "easter_offset", "offset": str(offset), "comparator": "eq"}
        self.assertTrue(build_condition(data).is_met)
        data["offset"] = str(offset + 1)
        self.assertFalse(build_condition(data).is_met)
        data["offset"] = str(offset - 1)
        self.assertFalse(build_condition(data).is_met)
