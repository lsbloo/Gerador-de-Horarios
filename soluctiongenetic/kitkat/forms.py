from django import forms


class CriterionForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    description = forms.CharField(max_length=254, help_text='Required. Description for critérion.')
    rate = forms.IntegerField(label="peso")
    
class KitKatUserForm(forms.Form):
    username = forms.CharField(label="username",max_length=100)
    password= forms.CharField(label="password", max_length=100)
    email = forms.EmailField(label="email", max_length=100)
    is_staff = forms.BooleanField(required=False)
    
    

