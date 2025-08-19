import mido
from django import forms

from .models import Carillon


def get_midi_ports():
    yield ("", "---------")
    for port in mido.get_output_names():
        yield (port, port)


class CarillonForm(forms.ModelForm):
    """This form allows the user to select a MIDI port from available ports."""

    port_name = forms.ChoiceField(
        widget=forms.Select,
        choices=get_midi_ports,
        required=False,
    )

    class Meta:
        model = Carillon
        fields = ["name", "port_name"]
