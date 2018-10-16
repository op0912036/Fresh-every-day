from django.shortcuts import render, redirect
from django.views.generic import View


# Register your models here.
class IndexView(View):
    '''首页'''
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        return render(request, 'index.html')
