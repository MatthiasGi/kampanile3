from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .carillon import Carillon


class Striker(models.Model):
    """
    A model representing a striker that acts as a proxy between rules and the
    carillon.
    """

    class CheckType(models.TextChoices):
        """Setting for how often the striker should check for rules to play."""

        MANUAL = "M", _("Check manually, no automatic checks")
        EVERY_MINUTE = "m", _("Check every minute")
        EVERY_QUARTER_HOUR = "q", _("Check every quarter hour")
        EVERY_HALF_HOUR = "h", _("Check every half hour")
        EVERY_HOUR = "H", _("Check every hour")

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )
    """The name of the striker for a friendly display."""

    carillon = models.ForeignKey(
        Carillon,
        on_delete=models.PROTECT,
        related_name="strikers",
        verbose_name=_("Carillon"),
    )
    """The carillon that this striker is associated with."""

    priority = models.IntegerField(
        default=0,
        verbose_name=_("Priority"),
        help_text=_(
            "The priority of this striker, used to determine if it should abort other strikers' songs."
        ),
    )
    """The priority of this striker for playing songs."""

    check_type = models.CharField(
        max_length=1,
        choices=CheckType,
        default=CheckType.MANUAL,
        verbose_name=_("Check type"),
        help_text=_("The type of check condition or interval."),
    )
    """The type of check: how often the striker should check for rules to play?"""

    def check_rules(self):
        """Check the rules of this striker and play a song if a rule applies."""
        messages = []
        for rule in self.rules.order_by("-priority"):
            if not rule.is_met:
                continue
            messages += rule.midi
            if rule.cancel_following:
                break
        if messages:
            self.carillon.play(messages, priority=self.priority)

    def get_absolute_url(self) -> str:
        return reverse("carillon:strikers:detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_checkable() -> models.QuerySet["Striker"]:
        """
        Return a queryset of strikers that should check for rules to play now.
        """
        minute = timezone.now().minute
        q = models.Q(check_type=Striker.CheckType.EVERY_MINUTE)
        if minute % 15 == 0:
            q |= models.Q(check_type=Striker.CheckType.EVERY_QUARTER_HOUR)
        if minute % 30 == 0:
            q |= models.Q(check_type=Striker.CheckType.EVERY_HALF_HOUR)
        if minute == 0:
            q |= models.Q(check_type=Striker.CheckType.EVERY_HOUR)
        return Striker.objects.filter(q).order_by("-priority")

    @staticmethod
    def run_checks() -> None:
        """Check all strikers that should check for rules to play now."""
        for striker in Striker.get_checkable():
            striker.check_rules()

    class Meta:
        verbose_name = _("Striker")
        verbose_name_plural = _("Strikers")
