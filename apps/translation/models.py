from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone
from apps.users.models import UserProfile


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(is_deleted=True)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(is_deleted=False)

    def dead(self):
        return self.exclude(is_deleted=False)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(is_deleted=False)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class AdminViewManager(models.Manager):
    pass


class SoftDeletionModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)
    with_deleted = AdminViewManager()

    class Meta:
        abstract = True

    def delete(self):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()


class Phrase(SoftDeletionModel):
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='phrase_usernames',
                                 null=True, blank=True)
    phrase_text = models.TextField()
    translation_text = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(UserProfile, related_name='likes', blank=True)
    complaint = models.PositiveIntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('phrase_detail',  kwargs={'pk': self.pk})

    def __str__(self):
        return self.phrase_text


class Translation(SoftDeletionModel):
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='translation_usernames',
                                 null=True, blank=True)
    phrase_text = models.ForeignKey(Phrase, on_delete=models.CASCADE)
    translate_text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    complaint = models.BooleanField(null=True, blank=True)
    likes = models.ManyToManyField(UserProfile, related_name='translation_likes', blank=True)
    votes = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('translation_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.translate_text

    def get_like_url(self):
        return reverse('translation_like', kwargs={'pk': self.pk})


class TranslationComment(SoftDeletionModel):
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_usernames',
                                 null=True, blank=True)
    translate = models.ForeignKey(Translation, on_delete=models.CASCADE, null=True)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('comment_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.comment



