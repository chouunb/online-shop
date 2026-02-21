from django import forms

from blog.models import Product



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','category', 'tags', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
            'placeholder': "Название (максимальная длина 150 символов)"
        }),
        'category': forms.Select(attrs={'class': 'form-control'}),
        'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        'image': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': 'Название товара:',
            'category': 'Категория:',
            'tags': 'Теги:',
            'description': 'Описание товара:',
            'image': 'Изображение товара'
        }
        help_texts = {
            'category': "- можно выбрать только одну категорию"
        }

    def clean_name(self):
        name=self.cleaned_data['name'].strip()

        if not name:
            raise forms.ValidationError('Название товара обязательно!')
        
        if len(name) < 3:
            raise forms.ValidationError('Название не должно быть короче 3 символов!')
        
        return name
