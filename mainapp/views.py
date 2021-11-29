from django.shortcuts import render
import authapp.models
import publicationapp.models

def main(request):
	print (request)
	content = {
		'test': 11111111111111
	}
	return render(request, 'mainapp/index.html', content)

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

def account(request):
	print (request)
	return render(request, 'mainapp/watch_account.html')

def account_edit(request):
	print (request)
	return render(request, 'mainapp/account_edit.html')

def pub_one(request):
	print (request)
	return render(request, 'mainapp/pub_one.html')

def pub_create_new(request):
	print (request)
	return render(request, 'mainapp/pub_create_new.html')

def pub_edit(request):
	print (request)
	return render(request, 'mainapp/pub_edit.html')

def support(request):
	print (request)
	return render(request, 'mainapp/send_to_support.html')

def become_an_author(request):
	print (request)
	return render(request, 'mainapp/application_to_become_an_author.html')

def become_a_teammemder(request):
	print (request)
	return render(request, 'mainapp/application_to_become_an_teammemder.html')

def help(request):
	print (request)
	return render(request, 'mainapp/help.html')

def adminRDF(request):
	print (request)
	return render(request, 'mainapp/admin.html')
