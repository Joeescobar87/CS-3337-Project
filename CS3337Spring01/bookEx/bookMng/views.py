from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from .models import MainMenu
from .forms import BookForm
from .forms import SearchForm
from .models import Book
from .models import Comment, AdditionalComments
from .forms import CommentForm, AdditionalCommentForm


from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


from django.contrib.auth.decorators import login_required


def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })


@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        comment_form = CommentForm(request.POST)
        if form.is_valid() and comment_form.is_valid():
            #form.save()
            book = form.save(commit=False)
            book.username = request.user
            book.save()
            comments = comment_form.save(commit=False)
            comments.book = book
            comments.user = request.user
            comments.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        comment_form = CommentForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted,
                      'comment_form': comment_form,
                  })


@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    comments = Comment.objects.filter(book=book)
    additional_comments = AdditionalComments.objects.filter(book=book)
    additional_comment_form = AdditionalCommentForm()
    if request.method == "POST":
        additional_comment_form = AdditionalCommentForm(request.POST)
        if additional_comment_form.is_valid():
            additional_comment = additional_comment_form.save(commit=False)
            additional_comment.book = book
            additional_comment.user = request.user
            additional_comment.save()
            return redirect('book_detail', book_id=book_id)
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'comments': comments,
                      'additional_comments': additional_comments,
                      'additional_comment_form': additional_comment_form,
                  })


@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })


@login_required(login_url=reverse_lazy('login'))
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  })

@login_required(login_url=reverse_lazy('login'))
def aboutus(request):
    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })

@login_required(login_url=reverse_lazy('login'))
def searchbook(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            books = Book.objects.filter(name__icontains =name)
            for b in books:
                b.pic_path = b.picture.url[14:]
            return render(request,
                          'bookMng/searchresults.html',
                          {
                              'item_list': MainMenu.objects.all(),
                              'form': form,
                              'books': books,
                          })
    else:
        form = SearchForm()
    return render(request,
                  'bookMng/searchbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                  })

