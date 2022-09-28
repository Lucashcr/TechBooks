from pipes import Template
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


from .models import Book, Subject


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
    
    def get(self, request, subject_slug, book_slug):
        try:
            book = Book.objects.get(slug=book_slug)
            subject = Subject.objects.get(slug=subject_slug)
            title = book.name
        except:
            book = None
            title = 'Livro não enontrado'
        
        extra_context = {
            'title': f'Techbooks - {title}',
            'book': book,
            'subject': subject,
            'section': '/#_por_que_julia'
        }
        
        return render(request, template_name='read_book.html', context=extra_context)
        
        
class ListBooks(TemplateView):
    template_name = 'book_list.html'

    def get(self, request):
        try:
            subject_list = Subject.objects.all()
            book_list = Book.objects.all()
        except:
            subject_list = None
            book_list = None
        
        extra_context = {
            'title': f'Techbooks - Livros',
            'book_list': book_list,
            'filtered': False,
            'subject_list': subject_list,
            'book_list': book_list
        }
        
        return render(request, template_name='book_list.html', context=extra_context)
    # model = Book
    # context_object_name = 'book_list'
    # queryset = Book.objects.all()
    # template_name = 'book_list.html'
    # context = {
    #     'title': f'Techbooks - Livros',
    #     'filtered': False,
    #     'subject_list': Subject.objects.all()
    # }


class ListSubjects(ListView):
    model = Subject
    context_object_name = 'subject_list'
    queryset = Subject.objects.all()
    template_name = 'subject_list.html'


class ListBooksBySubject(TemplateView):
    template_name = 'book_list.html'

    def get(self, request, subject_slug):
        extra_context = {}
        
        try:
            subject = Subject.objects.get(slug=subject_slug)
            extra_context['book_list'] = Book.objects.filter(subject_id=subject.id)
            extra_context['title'] = f'Techbooks - {subject.name}'
            extra_context["subject"] = subject
            extra_context['filtered'] = True
        except:
            extra_context['book_list'] = None
            extra_context['title'] = 'Livro não enontrado'
            extra_context['filtered'] = False
                
        return render(request, template_name='book_list.html', context=extra_context)


class SignUp(TemplateView):
    template_name = 'signup.html'
    extra_context = {}

    def get(self, request):
        self.extra_context['error'] = request.GET.get('error')
        return render(request, self.template_name, self.extra_context)

    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            username_exists = False
        else:
            username_exists = True
        
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            email_exists = False
        else:
            email_exists = True
            
        if username_exists or email_exists:
            return redirect('/signup/?error=1')

        if password != confirm_password:
            return redirect('/signup/?error=2')

        new_user = User(username=username, email=email, password=password)
        new_user.save()

        print('cadastrado com sucesso')