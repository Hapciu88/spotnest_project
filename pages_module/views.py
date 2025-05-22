from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import logging

logger = logging.getLogger("admin.logger")

class BaseView(View):
    http_method_names = []

    def render_template(self, template_name, context):
        if settings.DEBUG:
            return render(self.request, template_name, context)
        try:
            return render(self.request, template_name, context)
        except Exception as err:
            logger.error(f"[{self.__class__.__name__}] {err}")
            messages.error(self.request, 'There was an error loading the page.')
            raise err
            return redirect('/coming-soon')

class LandingView(View):
    http_method_names = ['get']
    __title = "SpotNest"

    context = {
        'title': __title,
    }

    def get(self, *args, **kwargs):
        try:
            return render(self.request, 'module_pages/landing_page.html', self.context)
        except Exception as err:
            logger.error(f"[ LandingView ] {err}")
            messages.error(self.request, 'There was an error loading the page.')
            raise err
            return redirect('/coming-soon')
