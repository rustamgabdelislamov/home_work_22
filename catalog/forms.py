import os

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import BooleanField
from django.template.defaultfilters import lower
from unicodedata import category

from .models import Product

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():  # Ключ (field_name) — это строка, обозначающая имя поля («title», «content», «price» и т.п.).Значение (field) — это экземпляр конкретного класса поля, например, CharField, IntegerField, BooleanField и т.д., наследующие от базового класса полей Django.
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']


    # def __init__(self, *args, **kwargs):
    #     super(ProductForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите имя'})
    #     self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание'})
    #     self.fields['image'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Загрузите изображение'})
    #     self.fields['category'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите цену'})


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        category = cleaned_data.get('category')

        lower_name = name.lower()
        lower_description = description.lower()

        if lower_name and lower_description and lower_name in FORBIDDEN_WORDS or lower_description in FORBIDDEN_WORDS:
            self.add_error('name', 'Недопустимые слова для имени или описания')

        if Product.objects.filter(name=name, category=category):
            raise ValidationError('Продукт с таким именем в данной категории существует')
        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    def clean_image(self):
        """
        Валидирует изображение на предмет правильного расширения и максимального размера файла.
        """
        image = self.cleaned_data.get('image')  # Получаем файл

        # Проверяем тип полученного объекта
        if isinstance(image, InMemoryUploadedFile):  # Проверяем, что это файл
            file_size = image.size  # Размер файла в байтах
            max_file_size = 5 * 1024 * 1024  # Максимальный размер файла (5 MB)

            # Ограничиваем максимальный размер файла
            if file_size > max_file_size:
                raise ValidationError(f'Размер файла превышает лимит ({max_file_size // (1024 * 1024)}MB)')

            # Проверяем расширение файла
            file_extension = os.path.splitext(image.name)[1].lower()  # Расширение файла
            allowed_extensions = ('.png', '.jpg')  # Разрешённые расширения

            if file_extension not in allowed_extensions:
                raise ValidationError(f'Можно загружать только файлы формата {", ".join(allowed_extensions)}')

        return image
