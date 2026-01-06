from django import forms


class ProductForm(forms.Form):
    name = forms.CharField(
        max_length=255, 
        label="Название товара:", 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': "Название (максимальная длина 150 символов)"
        })
    )

    description = forms.CharField(
        label="Описание товара:", 
        widget=forms.Textarea(attrs={
            'row': 3
        })
    )

    price = forms.IntegerField(
        label="Цена товара:",
    )

    def clean_name(self):
        name=self.cleaned_data['name'].strip()

        if not name:
            raise forms.ValidationError('Название товара обязательно!')
        
        if len(name) < 3:
            raise forms.ValidationError('Название не должно быть короче 3 символов!')
        
        return name