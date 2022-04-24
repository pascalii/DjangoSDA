import json
from uuid import uuid4

from django.core.exceptions import BadRequest
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from books.models import BookAuthor, Category


class AuthorListBaseView(View):
    template_name = "author_list.html"
    queryset = BookAuthor.objects.all()  # type: ignore

    def get(self, request: WSGIRequest, *args, **kwargs):
        context = {"authors": self.queryset}
        return render(request, template_name=self.template_name, context=context)


class CategoryListTemplateView(TemplateView):
    template_name = "category_list.html"
    extra_context = {"categories": Category.objects.all()}



def get_hello_world(request: WSGIRequest) -> HttpResponse:
    # return HttpResponse("Hello world")
    hello_str: str = "Hello world"
    return render(request, template_name="hello_world.html", context={"hello_var": hello_str})


def get_uuids_list_a(request: WSGIRequest) -> HttpResponse:
    uuids = [str(uuid4()) for _ in range(10)]
    # uuids_as_json = json.dumps(uuids)
    # return HttpResponse(uuids_as_json)
    return render(request, template_name="uuids_list.html", context={"uuids": uuids})


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