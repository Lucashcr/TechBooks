from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView, ListView
from django.contrib.auth import authenticate, login


from .models import Book


# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'
    extra_context = {'title': 'TechBooks'}

    
class Login(FormView):
    template_name = 'login.html'
    extra_context = {
        'title': 'TechBooks - Login', 
        'error': False
    }
    
    def get(self, request, *args, **kwargs):
        self.extra_context['error'] = kwargs.get('error')
        self.return_url = kwargs.get('return_url')
        print("URL de retorno:", kwargs.get('return_url'))
        return render(request, self.template_name, self.extra_context)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        auth = authenticate(username=username, password=password)
        
        if username is not None:
            login(request, auth)
            print(kwargs.get('return_url'))
            return redirect(request.return_url)
            # return render(request, self.template_name, self.extra_context)

    
class SubmitLogin(TemplateView):
    template_name = 'submit_login.html'
    extra_context = {'title': 'TechBooks - Login efetuado'}
    

class ReadBook(TemplateView):
    template_name = 'read_book.html'
    # login_required = True
    
    def get(self, request, book_id):
    #     if str(request.user) == 'AnonymousUser':
    #         print("URL de retorno:", request.path)
    #         return redirect('/login', return_url=request.path)
        
        # if book_code == 'think-julia':
        #     book_name = 'Julia Intro'
        #     book_url = 'https://juliaintro.github.io/JuliaIntroBR.jl/'
        #     is_page = True
        # elif book_code == 'python-para-devs':
        #     book_name = 'Python para desenvolvedores'
        #     book_url = '/books/python/python-para-desenvolvedores.pdf'
        #     is_page = False
        # else:
        #     book_name = 'Livro não encontrado'
        #     book_url = ''
        #     is_page = True

        try:
            book = Book.objects.get(id=book_id)
            title = book.name
        except:
            book = None
            title = 'Livro não enontrado'
        
        extra_context = {
            'title': f'Techbooks - {title}',
            'book': book
        }
        
        return render(request, template_name='read_book.html', context=extra_context)
        
        
class ListBooks(ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.all()
    template_name = 'book_list.html'
    
    # paginate_by = 100  # if pagination is desired
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = datetime.now()
    #     return context