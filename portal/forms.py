from django import forms


class FileUploadForm(forms.Form):
    data_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
