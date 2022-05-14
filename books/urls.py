from django.urls import path

from books.views import get_hello_world, get_uuids_list_a, get_uuids_list_b, get_argument_from_path, \
    get_arguments_from_query, check_http_query_type, get_headers, raise_error_for_fun, AuthorListBaseView, \
    CategoryListTemplateView, BooksListView, BookDetailsView, CategoryCreateFormView, BookCreateView, AuthorCreateView, \
    AuthorUpdateView


class BooksCreateView(object):
    pass


urlpatterns = [
    path('', get_hello_world, name="home"),
    path('uuids_a/', get_uuids_list_a, name="uuids_a"),
    path('uuids_b/', get_uuids_list_b, name="uuids_b"),
    path('path-args/<int:first_arg>/<str:second_arg>/<slug:third_arg>/', get_argument_from_path, name="path_args"),
    path('query-args/', get_arguments_from_query, name="query_args"),
    path('check-http-type/', check_http_query_type, name="check_http_type"),
    path('get-headers/', get_headers, name="get_headers"),
    path('raise-error/', raise_error_for_fun, name="raise_error"),
    path('author-list', AuthorListBaseView.as_view(), name="author-list"),
    path('category-list', CategoryListTemplateView.as_view(), name="category-list"),
    path('book-list', BooksListView.as_view(), name="book-list"),
    path('book-create', BookCreateView.as_view(), name="book-create"),
    path('book-details/<int:pk>/', BookDetailsView.as_view(), name="book-details"),
    path('category-create/', CategoryCreateFormView.as_view(), name="category_create"),
    path('author-create/', AuthorCreateView.as_view(), name="author_create"),
    path('author-update/<int:pk>/', AuthorUpdateView.as_view(), name="author_update"),
]

