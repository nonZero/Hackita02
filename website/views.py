import os.path

from django.conf import settings

from django.views.generic.base import TemplateView
import markdown


def read_faq(n):
    with open(os.path.join(os.path.dirname(__file__), 'faq%d.md' % n)) as f:
        return markdown.markdown(f.read())


def get_faq():
    return [read_faq(n + 1) for n in range(2)]


FAQ = get_faq()


class HomeView(TemplateView):
    template_name = 'website/home.html'
    name = 'home'


class ProgramView(TemplateView):
    template_name = 'website/program.html'
    name = 'program'


class FAQView(TemplateView):
    template_name = 'website/faq.html'
    name = 'faq'

    def get_context_data(self, **kwargs):
        d = super(FAQView, self).get_context_data(**kwargs)
        d['faq'] = get_faq() if settings.DEBUG else FAQ
        return d
