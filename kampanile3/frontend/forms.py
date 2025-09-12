from crispy_forms.layout import HTML, Div, Layout, Submit
from django.utils.translation import gettext as _


class FormAction(Layout):
    def __init__(
        self, cancel_url=None, cancel_label=_("Cancel"), submit_label=_("Save")
    ):
        super().__init__(
            Div(
                Div(
                    HTML(
                        f"<a href='{cancel_url}' class='btn btn-outline-secondary d-block'>{cancel_label}</a>"
                    ),
                    css_class="col-5 col-sm-3 offset-sm-5",
                ),
                Div(
                    Submit("save", submit_label, css_class="d-block w-100"),
                    css_class="col-6 offset-1 offset-sm-0 col-sm-4",
                ),
                css_class="row gx-2 mb-3",
            )
        )
