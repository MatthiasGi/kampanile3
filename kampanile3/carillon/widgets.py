from django.forms import Textarea


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

    class Media:
        js = ["carillon/alert_helper.js"]
