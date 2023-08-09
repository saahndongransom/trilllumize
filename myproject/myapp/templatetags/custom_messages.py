from django import template
from django.contrib import messages

register = template.Library()

@register.simple_tag(takes_context=True)
def show_messages(context):
    request = context['request']
    return template.loader.render_to_string('messages.html', {'messages': messages.get_messages(request)})
