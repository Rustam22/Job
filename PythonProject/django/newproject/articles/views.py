from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import engines
from django.views.generic.base import TemplateView



def hello(request):
    return HttpResponse("<div style='color: red;'> Hello, world. You're at the polls index. </div>")


def helloTemplate(request):
    name = 'Rustam'
    html = render_to_string('hello.html', {'name': name})
    #django_engine = engines['django']
    #template = django_engine.from_string("Hello {{ name }}!")
    return HttpResponse(html)



class HelloTemplate(TemplateView):
        template_name = 'hello_class.html'

        def get_context_data(self, **kwargs):
            context = super(HelloTemplate, self).get_context_data(**kwargs)
            context['name'] = 'Shamrun'
            context['surname'] = 'Karimov'
            return context



#-----------------------------Advanced views and urls-----------------------------#

''' 
from . models import Article

def articles(request):
    return render_to_string('articles.html', {'articles': Article.objects.all()})

def article(request, article_id=1):
    return render_to_string('article.html', {'article': Article})

'''