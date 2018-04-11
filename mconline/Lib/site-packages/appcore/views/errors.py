"""Implements core app views"""

from django.views.generic import TemplateView
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseNotAllowed


class Handler404(TemplateView):
    template_name = '404.html'

    @classmethod
    def as_error_view(cls):
        v = cls.as_view()

        def view(request):
            r = v(request)
            if not hasattr(r, 'render'):
                return HttpResponseNotAllowed(['GET'])
            r.render()
            return HttpResponseNotFound(r)

        return view


class Handler500(TemplateView):
    template_name = '500.html'

    @classmethod
    def as_error_view(cls):
        v = cls.as_view()

        def view(request):
            r = v(request)
            if not hasattr(r, 'render'):
                return HttpResponseNotAllowed(['GET'])
            r.render()
            return HttpResponseServerError(r)

        return view
