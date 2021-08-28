from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


class EntryQuerySet(models.QuerySet):
    def get_or_none(self, *args, **kwargs):
        try:
            return super(EntryQuerySet, self).get(*args, **kwargs)
        except ObjectDoesNotExist:
            return None

    def delete(self):
        """
        論理削除    
        Model.objects.all().delete()
        :return:
        削除した件数
        """
        return super(EntryQuerySet, self).update(deleted_at=timezone.now())

    def delete_hard(self):
        """
        物理削除
        Model.objects.all().delete_hard()
        :return:
        削除した件数
        """
        return super(EntryQuerySet, self).delete()


class EntryModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def get_queryset(self):
        return EntryQuerySet(self.model)


class EntryModelManagerActive(EntryModelManager):
    def get_queryset(self):
        return EntryQuerySet(self.model).filter(deleted_at=None)


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
    updated_at = models.DateTimeField(
        verbose_name='公開日時',
        null=True,
        blank=True
    )
    edited_at = models.DateTimeField(
        verbose_name='更新日時',
        null=True,
        blank=True
    )
    deleted_at = models.DateTimeField(
        verbose_name='削除日時',
        null=True,
        blank=True,
        default=None
    )

    """
    通常検索で利用する Manager
    論理削除されたものが表示されない
    """
    objects = EntryModelManagerActive()
    """
    全体検索で利用する Manager
    論理削除されたものも含めて表示する
    """
    entire = EntryModelManager()

    def delete(self, using=None, keep_parents=False, is_hard=False):
        if is_hard:
            return super().delete(using, keep_parents)
        else:
            self.deleted_at = timezone.now()
            self.save(using)
            return 1, {}

    def delete_hard(self, using=None, keep_parents=False):
        self.delete(using, keep_parents, is_hard=True)

    class Meta:
        db_table = 'entry'
        verbose_name = '記事'
        verbose_name_plural = '記事'
