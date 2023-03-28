from django.http import JsonResponse
from django.shortcuts import render


def main_page(request):
    return JsonResponse({'status': 'ok'}, status=200)
