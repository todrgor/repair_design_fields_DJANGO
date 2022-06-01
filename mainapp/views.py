from django.shortcuts import render
from authapp.models import *
from publicationapp.models import *

def main(request):
	return render(request, 'mainapp/index.html')
