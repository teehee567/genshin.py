"""Starrail chronicle notes."""
import datetime
import typing

from genshin.models.model import Aliased, APIModel

__all__ = ["StarRailExpedition", "StarRailNote"]


class StarRailExpedition(APIModel):
    """StarRail expedition."""

    avatars: typing.List[str]
    status: typing.Literal["Ongoing", "Finished"]
    remaining_time: datetime.timedelta
    name: str

    @property
    def finished(self) -> bool:
        """Whether the expedition has finished."""
        return self.remaining_time <= datetime.timedelta(0)

    @property
    def completion_time(self) -> datetime.datetime:
        return datetime.datetime.now().astimezone() + self.remaining_time


class StarRailNote(APIModel):
    """StarRail chronicle note."""

    current_stamina: int
    max_stamina: int
    stamina_recover_time: datetime.timedelta
    accepted_epedition_num: int
    total_expedition_num: int
    expeditions: typing.Sequence[StarRailExpedition]

    current_train_score: int
    """Current daily training activity"""
    max_train_score: int
    """Max daily training activity"""

    current_rogue_score: int
    """Current simulated universe weekly points"""
    max_rogue_score: int
    """Max simulated universe weekly points"""

    remaining_weekly_discounts: int = Aliased("weekly_cocoon_cnt")
    """Remaining echo of war rewards"""
    max_weekly_discounts: int = Aliased("weekly_cocoon_limit")
    """Echo of war attempt limit"""

    current_reserve_stamina: int
    is_reserve_stamina_full: bool

    @property
    def stamina_recovery_time(self) -> datetime.datetime:
        """The time when stamina will be recovered."""
        return datetime.datetime.now().astimezone() + self.stamina_recover_time
