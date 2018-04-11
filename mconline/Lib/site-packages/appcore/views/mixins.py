"""Implements decorator chaining mixin for class based view"""

from django.contrib import messages
from django.http import JsonResponse


class DecoratorChainingMixin(object):
    def dispatch(self, *args, **kwargs):
        decorators = getattr(self, 'decorators', [])
        base = super(DecoratorChainingMixin, self).dispatch

        for decorator in decorators:
            base = decorator(base)
        return base(*args, **kwargs)


class FormMessageMixin(object):
    """
    Make it easy to display notification messages when using Class Based Views.
    """

    def delete(self, request, *args, **kwargs):
        message = None
        if hasattr(self, 'form_delete_message'):
            message = self.form_delete_message
        elif hasattr(self, 'form_valid_message'):
            message = self.form_valid_message
        if message is not None:
            messages.success(self.request, message)
        return super(FormMessageMixin, self).delete(request, *args, **kwargs)

    def form_valid(self, form):
        message = self.form_valid_message if hasattr(self, 'form_valid_message') else None
        if message is not None:
            messages.success(self.request, message)
        return super(FormMessageMixin, self).form_valid(form)

    def form_invalid(self, form):
        message = self.form_invalid_message if hasattr(self, 'form_invalid_message') else None
        if message is not None:
            messages.error(self.request, message)
        return super(FormMessageMixin, self).form_invalid(form)


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: In reality, you'll need to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets -- can be serialized as JSON.
        # You should implement this in your app.
        return context