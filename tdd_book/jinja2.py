from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.test import signals

from jinja2 import Environment
from jinja2 import Template as Jinja2Template


# Monkey-patch for Jinja templates so that template and context attrs could be used in tests
#   maybe move to signals ?
ORIGINAL_JINJA2_RENDERER = Jinja2Template.render
def instrumented_render(template_object, *args, **kwargs):
    context = dict(*args, **kwargs)
    signals.template_rendered.send(
                            sender=template_object,
                            template=template_object,
                            context=context
                        )
    return ORIGINAL_JINJA2_RENDERER(template_object, *args, **kwargs)
Jinja2Template.render = instrumented_render


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
