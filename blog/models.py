from django.db import models

class Blog(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок",
        help_text="Введите заголовок блога",
    )
    content = models.TextField(
        verbose_name="Содержимое", help_text="Введите содержимое блога"
    )
    preview = models.ImageField(
        upload_to="blog/image",
        verbose_name="Превью",
        help_text="Загрузите изображение для блога",
        blank=True,
        null=True,
    )
    created_at = models.DateField(
        verbose_name="Дата создания",
        help_text="Введите дату создания",
        auto_now_add=True,
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликован",
        help_text="Отметьте, если блог опубликован",
    )
    views_counter = models.PositiveIntegerField(
        default=0,
        verbose_name="Счетчик просмотров",
        help_text="Укажите количество просмотров",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "блог"
        verbose_name_plural = "блоги"
        ordering = [
            "title",
        ]
