from .directorium_condition import DirectoriumCondition
from .easter_offset_condition import EasterOffsetCondition
from .event_rank_condition import EventRankCondition
from .event_title_condition import EventTitleCondition
from .season_condition import SeasonCondition

CONDITIONS = {
    "season": SeasonCondition,
    "event_rank": EventRankCondition,
    "event_title": EventTitleCondition,
    "easter_offset": EasterOffsetCondition,
}

__all__ = [c.__name__ for c in CONDITIONS.values()]
__all__ += ["DirectoriumCondition"]
