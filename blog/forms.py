from django import forms

from blog.models import Product



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={
            'placeholder': "Название (максимальная длина 150 символов)"
        })
        }
        labels = {
            'name': 'Название товара:',
            'description': 'Описание товара:'
        }

    def clean_name(self):
        name=self.cleaned_data['name'].strip()

        if not name:
            raise forms.ValidationError('Название товара обязательно!')
        
        if len(name) < 3:
            raise forms.ValidationError('Название не должно быть короче 3 символов!')
        
        return name
