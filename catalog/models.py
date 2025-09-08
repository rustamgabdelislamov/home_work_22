from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', help_text='Введите наименование категории')
    description = models.TextField(verbose_name='Описание', help_text='Введите описание категории')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name',]


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', help_text='Введите наименование продукта')
    description = models.TextField(verbose_name='Описание', help_text='Введите описание продукта')
    image = models.ImageField(upload_to='catalog/image', verbose_name='Изображение',help_text='Загрузите изображение товара', blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name='Категория', help_text='Введите категорию продукта',on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField(verbose_name='Цена', help_text='Введите цену продукта')
    created_at = models.DateField(verbose_name='Дата создания', help_text='Введите дату создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    def __str__(self):
        return f'{self.category} {self.name} {self.price} руб.'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name', 'category', 'price',]

    # product1 = Product.objects.create(name='Infinix', description='RAM 8 ГБ, память 256 ГБ', )