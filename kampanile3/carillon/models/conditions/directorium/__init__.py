from .directorium_condition import DirectoriumCondition
from .event_rank_condition import EventRankCondition
from .season_condition import SeasonCondition

CONDITIONS = {
    "season": SeasonCondition,
    "event_rank": EventRankCondition,
}

__all__ = [c.__name__ for c in CONDITIONS.values()]
__all__ += ["DirectoriumCondition"]
