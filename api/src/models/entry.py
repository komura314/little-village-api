from django.db import models


class Entry(models.Model):
    CHOICE_DRAFT = (
        ('yes', '下書き'),
        ('no', '公開')
    )
    entry_id = models.AutoField(
        verbose_name='記事Id',
        primary_key=True
    )
    hatena_entry_id = models.BigIntegerField(
        verbose_name='はてな記事Id',
        unique=True
    )
    category = models.CharField(
        verbose_name='カテゴリ',
        max_length=100,
        null=True,
        blank=True,
        default=''
    )
    title = models.CharField(
        verbose_name='タイトル',
        max_length=200,
        null=True,
        blank=True,
        default=''
    )
    summary = models.CharField(
        verbose_name='サムネイル文',
        max_length=1000,
        null=True,
        blank=True,
        default=''
    )
    content_md = models.TextField(
        verbose_name='内容_MarkDown',
        null=True,
        blank=True,
        default='')
    content_html = models.TextField(
        verbose_name='内容_HTML',
        null=True,
        blank=True,
        default=''
    )
    draft = models.CharField(
        verbose_name='下書き区分',
        max_length=10,
        choices=CHOICE_DRAFT,
        null=True,
        blank=True,
        default='yes'
    )
    published_at = models.DateTimeField(
        verbose_name='公開日時',
        null=True,
        blank=True
    )
    edited_at = models.DateTimeField(
        verbose_name='作成日時',
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        verbose_name='更新日時',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'entry'
        verbose_name = '記事'
        verbose_name_plural = '記事'
