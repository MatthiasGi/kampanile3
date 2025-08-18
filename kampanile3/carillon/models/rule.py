from django.db import models
from django.utils.translation import gettext_lazy as _

from ..conditions import build_condition
from .song import Song


def validate_rule_condition(value):
    build_condition(value).validate()


class Rule(models.Model):
    """A rule that defines when and what a striker should play."""

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    """The name of the rule for a friendly display."""

    priority = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("Priority"),
        help_text=_("The priority of the rule. Higher values means firstly evaluated."),
    )
    """The priority of the rule, used to determine the order of evaluation."""

    cancel_following = models.BooleanField(
        default=False,
        verbose_name=_("Cancel following rules"),
        help_text=_(
            "If checked, no following rule with smaller priority will be executed if this rule applies."
        ),
    )
    """Whether to cancel following rules with smaller priority."""

    condition = models.JSONField(
        verbose_name=_("Condition"),
        help_text=_("A JSON object actually defining the condition."),
        default=dict,
        blank=True,
        validators=[validate_rule_condition],
    )
    """The JSON object describing the condition for the rule."""

    song = models.ForeignKey(
        Song,
        on_delete=models.RESTRICT,
        verbose_name=_("Song"),
        help_text=_("The song to play when the rule applies."),
        related_name="+",
        blank=True,
        null=True,
    )
    """The song to play when the rule applies. None is allowed for rules that abort playing sounds."""

    @property
    def parsed_condition(self):
        """Return the parsed condition object."""
        return build_condition(self.condition)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["priority"]
        verbose_name = _("Rule")
        verbose_name_plural = _("Rules")
