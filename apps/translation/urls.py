from django.urls import path
from .views import *
from apps.users.views import IndexView

# URL patterns for url/phrase/<path.name>
urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('create/', PhraseCreateView.as_view(), name='phrase_create'),
    path('list/', PhraseListView.as_view(), name='phrase_list'),
    path('<int:pk>/', PhraseDetailView.as_view(), name='phrase_detail'),
    path('<int:pk>/edit/', PhraseEditView.as_view(), name='phrase_edit'),
    path('<int:pk>/delete/', PhraseDeleteView.as_view(), name='phrase_delete'),
    path('like/', like_phrase, name='like_phrase'),

    path('translation/', TranslationListView.as_view(), name='translation_list'),
    path('translation/<int:pk>/', TranslationDetailView.as_view(), name='translation_detail'),
    path('translation/<int:pk>/like/', TranslationLikeToggle.as_view(), name='translation_like'),
    path('translation/<int:pk>/edit/', TranslationEditView.as_view(), name='translation_edit'),
    path('translation/<int:pk>/delete/', TranslationDeleteView.as_view(), name='translation_delete'),
    path('translation/comment/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path('translation/comment/<int:pk>/edit/', CommentEditView.as_view(), name='comment_edit'),
    path('translation/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]

