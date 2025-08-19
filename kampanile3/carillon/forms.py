import mido
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms
from django.urls import reverse
from django.utils.translation import gettext as _

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-10"
        if self.instance.pk:
            url = self.instance.get_absolute_url()
        else:
            url = reverse("carillon:carillons:list")
        self.helper.layout = Layout(
            Field("name"),
            Field("port_name"),
            Div(
                Div(
                    HTML(
                        f"<a href='{url}' class='btn btn-outline-secondary col-5 col-sm-2 offset-sm-6'>{_('Cancel')}</a>"
                    ),
                    Submit("save", _("Save"), css_class="col-6 offset-1 col-sm-3"),
                    css_class="col-12 col-sm-10 offset-sm-2 row",
                ),
                css_class="mb-3 row",
            ),
        )
