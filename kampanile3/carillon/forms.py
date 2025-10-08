import mido
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.urls import reverse
from frontend.forms import FormAction

from .models import Carillon, Rule, Song, Striker
from .widgets import RuleConditionWidget


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
        fields = ["name", "port_name", "active", "default", "volume"]

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
            Field("active"),
            Field("default"),
            Field("volume"),
            FormAction(cancel_url=url),
        )


class StrikerForm(forms.ModelForm):
    class Meta:
        model = Striker
        fields = ["name", "carillon", "priority", "check_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-10"
        if self.instance.pk:
            url = self.instance.get_absolute_url()
        else:
            url = reverse("carillon:strikers:list")
        self.helper.layout = Layout(
            Field("name"),
            Field("check_type"),
            Field("carillon"),
            Field("priority"),
            FormAction(cancel_url=url),
        )


class SongForm(forms.ModelForm):
    """Form for creating or updating a song."""

    class Meta:
        model = Song
        fields = ["name", "slug", "file", "transpose", "tempo_multiplier"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-10"
        if self.instance.pk:
            url = self.instance.get_absolute_url()
        else:
            url = reverse("carillon:songs:list")
        self.helper.layout = Layout(
            Field("name"),
            Field("slug"),
            Field("file"),
            Field("transpose"),
            Field("tempo_multiplier"),
            FormAction(cancel_url=url),
        )


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = [
            "striker",
            "name",
            "priority",
            "cancel_following",
            "condition",
            "song",
            "repeat",
        ]
        widgets = {
            "condition": RuleConditionWidget(),
            "striker": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        striker = kwargs.pop("striker", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-10"
        if self.instance.pk:
            url = self.instance.get_absolute_url()
        else:
            url = striker.get_absolute_url()
        self.helper.layout = Layout(
            Field("striker"),
            Field("name"),
            Field("priority"),
            Field("cancel_following"),
            Field("condition"),
            Field("song"),
            Field("repeat"),
            FormAction(cancel_url=url),
        )
