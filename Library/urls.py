"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

# from books.views import get_hello_world, get_uuids_list_a, get_uuids_list_b, get_argument_from_path, \
#     get_arguments_from_query, check_http_query_type, get_headers, raise_error_for_fun

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('books/', include('books.urls'))
    # path('', get_hello_world, name="home"),
    # path('uuids_a/', get_uuids_list_a, name="uuids_a"),
    # path('uuids_b/', get_uuids_list_b, name="uuids_b"),
    # path('path-args/<int:first_arg>/<str:second_arg>/<slug:third_arg>/', get_argument_from_path, name="path_args"),
    # path('query-args/', get_arguments_from_query, name="query_args"),
    # path('check-http-type/', check_http_query_type, name="check_http_type"),
    # path('get-headers/', get_headers, name="get_headers"),
    # path('raise-error/', raise_error_for_fun, name="raise_error"),
]

"""
ex. 21
"""
# if settings.DEBUG:
#     urlpatterns.append(path('admin/', admin.site.urls))