import board
import microcontroller
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.urls import reverse
from frontend.forms import FormAction

from .models import Input


def get_board_pins():
    yield ("", "---------")
    for pin in dir(board):
        if isinstance(getattr(board, pin), microcontroller.Pin):
            yield (pin, pin)


class InputForm(forms.ModelForm):
    """This form allows the user to select a board pin from available pins."""

    pin = forms.ChoiceField(
        widget=forms.Select,
        choices=get_board_pins,
        required=False,
    )

    class Meta:
        model = Input
        fields = ["name", "pin", "active", "pull", "striker", "behaviour"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-10"
        if self.instance.pk:
            url = self.instance.get_absolute_url()
        else:
            url = reverse("gpio:inputs:list")
        self.helper.layout = Layout(
            Field("name"),
            Field("pin"),
            Field("active"),
            Field("pull"),
            Field("striker"),
            Field("behaviour"),
            FormAction(cancel_url=url),
        )
