from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .carillon import Carillon


class Striker(models.Model):
    """
    A model representing a striker that acts as a proxy between rules and the
    carillon.
    """

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

    def get_absolute_url(self):
        return reverse("carillon:strikers:detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Striker")
        verbose_name_plural = _("Strikers")
