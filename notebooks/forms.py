from django import forms

from .models import Notebook


class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = [
            "label",
            "notebook_type",
            "cover_color",
            "cover_pattern",
            "label_font",
        ]
        widgets = {
            "label": forms.TextInput(
                attrs={"placeholder": "e.g. Machine Learning", "maxlength": 120}
            ),
            "notebook_type": forms.RadioSelect,
            "cover_color": forms.RadioSelect,
            "cover_pattern": forms.RadioSelect,
            "label_font": forms.RadioSelect,
        }
