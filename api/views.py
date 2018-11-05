from django.http import JsonResponse
from django.shortcuts import render


def index_api(request):
    return JsonResponse({'I':'SE'})
