from django import forms

from blog.models import Product



class ProductForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите теги через запятую'
        }),
        label="Теги"
    )
    class Meta:
        model = Product
        fields = ['name','category', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
            'placeholder': "Название (максимальная длина 150 символов)"
        }),
        'category': forms.Select(attrs={'class': 'form-control'}),
        'image': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': 'Название товара:',
            'category': 'Категория:',
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
    
    def clean_tags_input(self):
        """
        Разбивает строку на список тегов:
        - удаляет лишние пробелы вокруг
        - приводит к нижнему регистру
        """
        tags_str = self.cleaned_data.get('tags_input')
        tags = [tag.strip().lower() for tag in tags_str.split(',') if tag.strip()]
        return tags
