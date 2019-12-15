from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404


class AuthorRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.username != self.request.user:
            return HttpResponseForbidden()
        return super(AuthorRequiredMixin, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(self.model, pk=id_)
