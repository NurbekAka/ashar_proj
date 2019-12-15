from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.db.models import Q
from django.views.generic.edit import FormMixin
from .models import Phrase, Translation, TranslationComment
from .forms import PhraseCreateForm, CreateTranslationsForm, CreateCommentForm
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import AuthorRequiredMixin


def index(request):
    return HttpResponse('Hello World!')


class PhraseListView(ListView):
    model = Phrase
    template_name = 'phrase/phrase_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        result = Phrase.objects.all().order_by('-id')
        if query:
            result = Phrase.objects.filter(Q(phrase_text__icontains=query))
        return result


class PhraseCreateView(LoginRequiredMixin, CreateView, FormMixin):
    template_name = 'phrase/phrase_create.html'
    form_class = PhraseCreateForm
    context_object_name = 'phrase'

    def get_success_url(self):
        return reverse('phrase_list')

    def form_valid(self, form):
        phrase = form.save(commit=False)
        phrase.username = self.request.user
        phrase.save()
        return super(PhraseCreateView, self).form_valid(form)


class PhraseDetailView(FormMixin, DetailView):
    model = Phrase
    template_name = 'phrase/phrase_detail.html'
    form_class = CreateTranslationsForm
    context_object_name = 'phrase'

    def get_context_data(self, *args, **kwargs):
        context = super(PhraseDetailView, self).get_context_data(**kwargs)
        context['translations'] = Translation.objects.filter(phrase_text=self.object).order_by('-id')

        is_liked = False
        phrase = self.object
        if phrase.likes.filter(id=self.request.user.id).exists():
            is_liked = True
        likes_number = phrase.likes.all().count()
        context['likes_number'] = likes_number
        context['is_liked'] = is_liked
        return context

    def get_success_url(self):
        return reverse('phrase_detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        translation = form.save(commit=False)
        translation.username = self.request.user
        translation.phrase_text = self.get_object()
        translation.save()
        return super(PhraseDetailView, self).form_valid(form)


# Later will rewrite in class based view.
def like_phrase(request):
    phrase = get_object_or_404(Phrase, id=request.POST.get('phrase_id'))
    is_liked = False
    if phrase.likes.filter(id=request.user.id).exists():
        phrase.likes.remove(request.user)
        is_liked = False
    else:
        phrase.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(phrase.get_absolute_url())


class PhraseEditView(LoginRequiredMixin, UpdateView):
    model = Phrase
    template_name = 'phrase/phrase_create.html'
    form_class = PhraseCreateForm
    context_object_name = 'edited'
    raise_exception = True

    def get_success_url(self, **kwargs):
        return reverse('phrase_detail', kwargs={'pk': self.kwargs['pk']})


class PhraseDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Phrase
    template_name = 'phrase/phrase_delete.html'
    raise_exception = True

    def get_success_url(self):
        return reverse('phrase_list')


class TranslationListView(ListView):
    model = Translation
    template_name = 'translation/translation_list.html'
    queryset = Translation.objects.all().order_by('-id')


class TranslationDetailView(FormMixin, DetailView):
    model = Translation
    form_class = CreateCommentForm
    template_name = 'translation/translation_detail.html'

    def get_success_url(self):
        return reverse('translation_detail', kwargs={'pk': self.object.id})

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Translation, pk=id_)

    def get_context_data(self, **kwargs):
        context = super(TranslationDetailView, self).get_context_data(**kwargs)
        context['comments'] = TranslationComment.objects.filter(translate=self.object).order_by('-id')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.username = self.request.user
        comment.translate = self.get_object()
        comment.save()
        return super(TranslationDetailView, self).form_valid(form)


class TranslationLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        id_ = self.kwargs.get("pk")
        obj = get_object_or_404(Translation, pk=id_)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


class TranslationEditView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    template_name = 'translation/translation_edit.html'
    form_class = CreateTranslationsForm
    raise_exception = True
    model = Translation

    def form_valid(self, form):
        return super().form_valid(form)


class TranslationDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Translation
    template_name = 'translation/translation_delete.html'
    raise_exception = True

    def get_success_url(self):
        return reverse('phrase_list')


class CommentDetailView(LoginRequiredMixin, DetailView):
    model = TranslationComment
    template_name = 'translation/comment_detail.html'
    raise_exception = True


class CommentEditView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    template_name = 'translation/comment_edit.html'
    form_class = CreateCommentForm
    model = TranslationComment
    raise_exception = True

    def form_valid(self, form):
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = TranslationComment
    template_name = 'translation/comment_delete.html'
    raise_exception = True

    def get_success_url(self):
        return reverse('translation_list')

