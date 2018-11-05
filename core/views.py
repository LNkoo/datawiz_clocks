from django.http import HttpResponse
from django.shortcuts import render


def index_core(request):
    return HttpResponse('<h1>Hello world</h1>')
