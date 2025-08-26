from .directorium_condition import DirectoriumCondition
from .easter_offset_condition import EasterOffsetCondition
from .event_rank_condition import EventRankCondition
from .event_title_condition import EventTitleCondition
from .season_condition import SeasonCondition

CONDITIONS = [
    EasterOffsetCondition,
    EventRankCondition,
    EventTitleCondition,
    SeasonCondition,
]
__all__ = [c.__name__ for c in CONDITIONS]
__all__ += ["DirectoriumCondition"]
