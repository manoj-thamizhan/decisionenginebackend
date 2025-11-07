# forms.py
from django import forms

class RuleSchemaUploadForm(forms.Form):
    excel_file = forms.FileField(
        label="Excel file (.xlsx)",
        help_text="Upload an .xlsx file whose header row contains column names matching the schema."
    )
