from django import forms
from .models import Phrase, Translation, TranslationComment


class PhraseCreateForm(forms.ModelForm):
    class Meta:
        model = Phrase
        fields = ('phrase_text',)


class CreateTranslationsForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ('translate_text',)


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = TranslationComment
        fields = ('comment',)
