import json
from uuid import uuid4

from django.core.exceptions import BadRequest
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
from books.models import BookAuthor, Category, Book
from books.forms import CategoryForm, BookForm, AuthorForm

import logging
logger = logging.getLogger("Igor")



class AuthorListBaseView(View):
    template_name = "author_list.html"
    queryset = BookAuthor.objects.all()  # type: ignore

    def get(self, request: WSGIRequest, *args, **kwargs):
        # logger.debug(f"{request} ---")
        context = {"authors": self.queryset}
        return render(request, template_name=self.template_name, context=context)


class CategoryListTemplateView(TemplateView):
    template_name = "category_list.html"
    extra_context = {"categories": Category.objects.all()}

class BooksListView(ListView):
    template_name = "books_list.html"
    model = Book
    paginate_by = 10


class BookDetailsView(DetailView):
    template_name = "book_detail.html"
    model = Book

    def get_object(self, **kwargs):
        return get_object_or_404(Book, id=self.kwargs.get("pk"))

class CategoryCreateFormView(FormView):
    template_name = "category_form.html"
    form_class = CategoryForm
    success_url = reverse_lazy("category_list")

    def form_invalid(self, form):
        logger.critical(f'FORM CRITICAL ERROR, MORE INFO {form}')
        return super().form_invalid(form)

    def form_valid(self, form):
        result = super().form_valid(form)
        logger.info(f"form = {form}")
        logger.info(f"form.cleaned_data = {form.cleaned_data}")  # cleaned means with removed html indicators
        check_entity = Category.objects.create(**form.cleaned_data)
        logger.info(f"check_entity-id={check_entity.id}")
        return result

class AuthorCreateView(CreateView):
    template_name = "author_form.html"
    form_class = AuthorForm
    success_url = reverse_lazy("authors_list")

class AuthorUpdateView(UpdateView):
    template_name = "author_form.html"
    form_class = AuthorForm
    success_url = reverse_lazy("authors_list")

    def get_object(self, **kwargs):
        return get_object_or_404(BookAuthor, id=self.kwargs.get("pk"))

class BookCreateView(CreateView):
    template_name = "book_form.html"
    form_class = BookForm
    success_url = reverse_lazy("book-list")

class BookUpdateView(UpdateView):
    template_name = "book_form.html"
    form_class = BookForm
    success_url = reverse_lazy("books_list")

    def get_object(self, **kwargs):
        return get_object_or_404(Book, id=self.kwargs.get("pk"))

def get_hello_world(request: WSGIRequest) -> HttpResponse:
    # return HttpResponse("Hello world")
    hello_str: str = "Hello world"
    return render(request, template_name="hello_world.html", context={"hello_var": hello_str})


def get_uuids_list_a(request: WSGIRequest) -> HttpResponse:
    uuids = [str(uuid4()) for _ in range(10)]
    # uuids_as_json = json.dumps(uuids)
    # return HttpResponse(uuids_as_json)
    return render(request, template_name="uuids_a.html", context={"uuids": uuids})


def get_uuids_list_b(request: WSGIRequest) -> JsonResponse:
    uuids = [str(uuid4()) for _ in range(10)]
    return JsonResponse({"uuids": uuids})


def get_argument_from_path(request: WSGIRequest, first_arg: int, second_arg: str, third_arg: str) -> HttpResponse:
    """
    ex. 13
    """
    return HttpResponse(f"first_arg={first_arg}, second_arg={second_arg}, third_arg={third_arg}")


def get_arguments_from_query(request: WSGIRequest) -> HttpResponse:
    a = request.GET.get("a")
    b = request.GET.get("b")
    c = request.GET.get("c")
    print(type(a))  # str - type casting needed
    print(type(b))  # str
    print(type(c))  # str
    return HttpResponse(f"a={a}, b={b}, c={c}")


@csrf_exempt  # here with that decorator we turn off CSRF in that function
def check_http_query_type(request: WSGIRequest) -> HttpResponse:
    """
    Remember to turn off CSRF token, ONLY FOR TESTS - for a while
    """
    # query_type = "?"
    # if request.method == "GET":
    #     query_type = "to jest GET - tutaj nie powinnismy dodawac i czytac BODY"
    # elif request.method == "POST":
    #     query_type = "to jest POST - tutaj dane leca w BODY"
    # elif request.method == "PUT":
    #     query_type = "to jest PUT - tutaj dane leca w BODY"
    # elif request.method == "DELETE":
    #     query_type = "to jest DELETE - tutaj nie powinnismy dodawac i czytac BODY"
    # """
    # haslo ciekawostka - model dojrzalosci Richardsona
    # https://devkr.pl/2018/04/10/restful-api-richardson-maturity-model/
    # """
    # return HttpResponse(query_type)
    return render(request, template_name="methods.html", context={})


def get_headers(request: WSGIRequest) -> JsonResponse:
    """
    HTTP - text protocol
            HEADERS - some data as dict
            \n\n
            BODY - some data as dict
    """
    headers = request.headers
    return JsonResponse({"headers": dict(headers)})


def raise_error_for_fun(request: WSGIRequest):
    raise BadRequest("My error")
    # return HttpResponse()