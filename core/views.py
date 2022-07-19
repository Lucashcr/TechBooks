from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, View
from django.contrib.auth import authenticate, login, logout


from .models import Book


# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'
    extra_context = {'title': 'TechBooks'}

    
class Login(FormView):
    template_name = 'login.html'
    extra_context = {
        'title': 'TechBooks - Login', 
    }
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            _next = request.GET.get('next')
            return redirect(_next if _next is not None else '/books/')
        
        self.extra_context['error'] = request.GET.get('error')
        return render(request, self.template_name, self.extra_context)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        auth = authenticate(username=username, password=password)
        
        if auth is not None:
            login(request, auth)
            _next = request.GET.get('next')
            return redirect(_next if _next is not None else '/books/')
        else:
            _next = request.GET.get('next')
            return redirect(f'/login/?{f"next={_next}&" if _next is not None else ""}error=1')        
        
        
class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')
    

class ReadBook(TemplateView):
    template_name = 'read_book.html'
    
    def get(self, request, book_id):
        # if str(request.user) == 'AnonymousUser':
        #     print("URL de retorno:", request.path)
        #     return redirect('/login', return_url=request.path)
        
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