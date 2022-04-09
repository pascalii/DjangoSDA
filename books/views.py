from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest

def get_hello(request: WSGIRequest) -> HttpResponse:
    return HttpResponse("Hello world!")


def get_uuids_a(request: WSGIRequest) -> HttpResponse:
