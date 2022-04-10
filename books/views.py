from uuid import uuid4

from django.shortcuts import render

from django.django.core.handlers.wsgi import WSGIRequest
from django.django.http.response import HttpResponse, JsonResponse


def get_hello(request: WSGIRequest) -> HttpResponse:
    return HttpResponse("Hello world!")


def get_uuids_a(request: WSGIRequest) -> HttpResponse:
    uuids = [f"{uuid4()}" for _ in range(10)]
    return HttpResponse(f"uuids={uuids}")

def get_uuids_b(request: WSGIRequest) -> JsonResponse:
    uuids = [f"{uuid4()}" for _ in range(10)]
    return JsonResponse({"uuids":uuids})

def get_argument_from_path(request: WSGIRequest, x: int, y: str, z: str) -> HttpResponse:
    return HttpResponse(f"x = {x}, y = {y}, z = {z}")
