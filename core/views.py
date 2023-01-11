from django.shortcuts import redirect, render, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, View
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.exceptions import ValidationError

import random

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
            _next = request.session.get('next')
            return redirect(_next if _next is not None else '/books/')
        
        self.extra_context['error'] = request.session.get('error')
        return render(request, self.template_name, self.extra_context)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        auth = authenticate(username=username, password=password)
        
        if auth is not None:
            login(request, auth)
            _next = request.session.get('next')
            return redirect(_next if _next is not None else '/books/')
        else:
            _next = request.GET.get('next')
            request.session['error'] = 1
            request.session['next'] = request.session.get('next')
            return redirect(f'/login/')
        
        
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
            subject = None
            title = 'Livro não enontrado'
        
        extra_context = {
            'title': f'Techbooks - {title}',
            'book': book,
            'subject': subject,
            'section': ''
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


class ListSubjects(ListView):
    model = Subject
    context_object_name = 'subject_list'
    queryset = sorted(Subject.objects.all(), key=lambda item: item.name)
    template_name = 'subject_list.html'


class ListBooksBySubject(TemplateView):
    template_name = 'book_list.html'

    def get(self, request, subject_slug):
        extra_context = {}
        
        try:
            subject = Subject.objects.get(slug=subject_slug)
            extra_context['book_list'] = sorted(
                Book.objects.filter(subject_id=subject.id),
                key=lambda item: item.name
            )
            extra_context['title'] = f'Techbooks - {subject.name}'
            extra_context['subject'] = subject
            extra_context['filtered'] = True
        except:
            extra_context['title'] = 'Livro não enontrado'
            extra_context['filtered'] = False
            extra_context['book_list'] = None
                
        return render(request, template_name='book_list.html', context=extra_context)


class SignUp(TemplateView):
    template_name = 'signup.html'
    extra_context = {}

    def get(self, request):
        self.extra_context['error'] = request.session.get('error')
        msg = request.session.get('msg')
        if msg:
            self.extra_context['msg'] = msg
        self.extra_context['username'] = request.GET.get('username')
        return render(request, self.template_name, self.extra_context)

    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        
        new_user = User(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name
        )
        
        try:
            User.objects.get(username=new_user.username)
        except User.DoesNotExist:
            username_exists = False
        else:
            username_exists = True
        
        try:
            User.objects.get(email=new_user.email)
        except User.DoesNotExist:
            email_exists = False
        else:
            email_exists = True
            
        if username_exists or email_exists:
            request.session['error'] = 1
            return redirect('/signup/')

        if password != confirm_password:
            request.session['error'] = 2
            return redirect('/signup/')

        try:
            password_validation.validate_password(new_user.password, new_user)
        except ValidationError as msg:
            request.session['error'] = 3
            request.session['msg'] = tuple(msg)

            return redirect('/signup/')

        confirm_code = str(random.randint(100000, 999999))
        new_user.email_user(
            'Teste',
            f'Codigo de confirmação - {confirm_code}',
            'lucash.rocha123@gmail.com'
        )

        request.session['confirm_code'] = confirm_code
        request.session['new_user'] = dict(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name
        )

        return redirect('/confirm/')


class Confirm(View):
    extra_context = {
        'title': 'TechBooks - Confirmar email', 
    }

    def get(self, request, *args, **kwargs):
        self.extra_context['error'] = request.session.get('error')
        return render(request, 'confirm.html', self.extra_context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('confirm_code') == request.session['confirm_code']:
            new_user = request.session['new_user']
            print(new_user['password'])
            User(
                username = new_user['username'],
                email = new_user['email'],
                first_name = new_user['first_name'],
                last_name = new_user['last_name'],
                password = new_user['password']
            ).save()
            request.session['error'] = 2
            return redirect('/login/')
        else:
            request.session['error'] = 1
            return redirect('/confirm/')
