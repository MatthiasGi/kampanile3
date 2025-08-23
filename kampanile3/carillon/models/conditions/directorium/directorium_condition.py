from django.conf import settings

from ..condition import Condition


class DirectoriumCondition(Condition):
    """Internal condition as superclass for everything that has a directorium."""

    @property
    def directorium(self):
        return settings.DIRECTORIUM
