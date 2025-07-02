from django.views.generic import TemplateView

from app.constants import PAGES_NAMES


class IndexView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = PAGES_NAMES['home_page']

        return context

class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = PAGES_NAMES['about_page']

        return context