from django.forms import Textarea

from .models.conditions import date, directorium, logic


class RuleConditionWidget(Textarea):
    template_name = "carillon/widgets/rule_condition.html"

    def __init__(self, attrs=None):
        default_attrs = {
            "class": "font-monospace",
            "rows": 20,
            "autocomplete": "off",
            "autocorrect": "off",
            "autocapitalize": "off",
            "spellcheck": "false",
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def get_context(self, *attrs, **kwargs):
        context = super().get_context(*attrs, **kwargs)
        modules = (logic, date, directorium)
        condition_groups = [[c.meta for c in m.CONDITIONS] for m in modules]
        context.update({"condition_groups": condition_groups})
        return context

    class Media:
        js = ["frontend/alert_helper.js"]
