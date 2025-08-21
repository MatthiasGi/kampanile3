from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..conditions import build_condition
from .song import Song


def validate_rule_condition(value):
    build_condition(value).validate()


class Rule(models.Model):
    """A rule that defines when and what a striker should play."""

    class RepeatSettings(models.TextChoices):
        OFF = "o", _("Off")
        HOURS12 = "h12", _("For every hour once 12-based")
        HOURS24 = "h24", _("For every hour once 24-based")
        MINUTES15 = "m15", _("For every 15 minutes")
        MINUTES30 = "m30", _("For every 30 minutes")

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

    repeat = models.CharField(
        max_length=3,
        choices=RepeatSettings,
        default=RepeatSettings.OFF,
        verbose_name=_("Repeat"),
        help_text=_(
            "How often the played song should be repeated if the rule applies."
        ),
    )
    """The song can optionally be repeated based on the selected setting."""

    @property
    def parsed_condition(self):
        """Return the parsed condition object."""
        return build_condition(self.condition)

    def get_absolute_url(self):
        return reverse("carillon:rules:detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["priority"]
        verbose_name = _("Rule")
        verbose_name_plural = _("Rules")
