from django import forms


class FileForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    password = forms.CharField(max_length=20, required=False,
                               help_text="This will allow sharing via additional link"
                                         " only accessible with a password")