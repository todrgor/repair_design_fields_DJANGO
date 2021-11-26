from django.shortcuts import render

def main(request):
	print (request)
	return render(request, 'mainapp/index.html')

def repairs(request):
	print (request)
	return render(request, 'mainapp/watch_repairs.html')

def designs(request):
	print (request)
	return render(request, 'mainapp/watch_designs.html')

def lifehacks(request):
	print (request)
	return render(request, 'mainapp/watch_lifehacks.html')

def saved(request):
	print (request)
	return render(request, 'mainapp/watch_saved.html')