from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView
from django.contrib.auth.decorators import login_required


# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'
    extra_context = {'title': 'TechBooks'}

    
class Login(FormView):
    template_name = 'login.html'
    extra_context = {'title': 'TechBooks - Login', 'error': False}
    
    def get(self, request, *args, **kwargs):
        self.extra_context['error'] = kwargs.get('error')
        print(self.extra_context['error'])
        return render(request, self.template_name, self.extra_context)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username != 'lucas' or password != '123':
            return self.get(request, error=True)
        else:
            return redirect('/login/submit')

    
class SubmitLogin(TemplateView):
    template_name = 'submit_login.html'
    extra_context = {'title': 'TechBooks - Login efetuado'}