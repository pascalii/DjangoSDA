from uuid import uuid4

from django.core.exceptions import BadRequest
from django.shortcuts import render

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def get_hello(request: WSGIRequest) -> HttpResponse:
    hello = "Hello world!"
    return render(request, template_name="hello_world.html", context={"hello_var": hello})


def get_uuids_a(request: WSGIRequest) -> HttpResponse:
    uuids = [f"{uuid4()}" for _ in range(10)]
    return render(request, template_name="uuids_a.html", context={"elements": uuids})
    # return HttpResponse(f"uuids={uuids}")

def get_uuids_b(request: WSGIRequest) -> JsonResponse:
    uuids = [f"{uuid4()}" for _ in range(10)]
    return JsonResponse({"uuids":uuids})

def get_argument_from_path(request: WSGIRequest, x: int, y: str, z: str) -> HttpResponse:
    return HttpResponse(f"x = {x}, y = {y}, z = {z}")

def get_arguments_from_query(request: WSGIRequest) -> HttpResponse:
    a = request.GET.get("a")
    b = request.GET.get("b")
    c = request.GET.get("c")
    print(type(int(a)))
    return HttpResponse(f"a = {a}, b = {b}, c = {c}")

@csrf_exempt
def check_http_query_type(request: WSGIRequest) -> HttpResponse:
    # query_type = 'Unknown'
    # if request.method == "GET":
    #     query_type = "this is GET"
    # elif request.method == "POST":
    #     query_type = "this is POST"
    # elif request.method == "DELETE":
    #     query_type = "this is DELETE"
    # return HttpResponse(query_type)
    return render(request, template_name="methods.html", context={})


def get_headers(request: WSGIRequest) -> JsonResponse:
    our_headers = request.headers
    return JsonResponse({"headers": dict(our_headers)})


def raise_error_for_fun(request: WSGIRequest) -> HttpResponse:
    if request.method != "GET":
        raise BadRequest("method not allowed")
    return HttpResponse("all GIT")