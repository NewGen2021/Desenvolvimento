from django import forms

class RegistrarAdministradorForm(forms.Form):
    nome = forms.CharField(widget=forms.TextInput(
            attrs={'required': 'true', 'id': 'id_nome_gerente'}))
    """ senha = forms.CharField(widget=forms.TextInput(
            attrs={'required': 'true', 'id': 'id_senha_gerente'})) """

    # class Meta:
    #     fields= ["cidade", ""]