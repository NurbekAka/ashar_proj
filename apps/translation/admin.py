from django.contrib import admin
from django.contrib.admin.actions import delete_selected
from .models import Phrase, Translation, TranslationComment
from apps.users.models import UserProfile


class PhraseAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return Phrase.all_objects.all()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        obj.hard_delete()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    actions = ["delete_object"]

    def delete_object(self, request, queryset):
        queryset.hard_delete()

    delete_selected.short_description = "Delete selected objects"


class TranslationCommentAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return TranslationComment.all_objects.all()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        obj.hard_delete()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    actions = ["delete_object"]

    def delete_object(self, request, queryset):
        queryset.hard_delete()

    delete_selected.short_description = "Delete selected objects"


class TranslationAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return Translation.all_objects.all()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        obj.hard_delete()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    actions = ["delete_object"]

    def delete_object(self, request, queryset):
        queryset.hard_delete()

    delete_selected.short_description = "Delete selected objects"


admin.site.register(UserProfile)
admin.site.register(Phrase, PhraseAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(TranslationComment, TranslationCommentAdmin)


