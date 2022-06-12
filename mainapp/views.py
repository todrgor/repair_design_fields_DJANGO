from django.shortcuts import render
from authapp.models import *
from publicationapp.models import *
from publicationapp.views import order_pubs_by_property

def main(request):
	saved_pubs_count = SavedPubs.objects.filter(saver=request.user).count() if request.user.is_authenticated else None

	pubs = Publication.objects.all()
	first_author = second_author = third_author = None
	if pubs:
		savest_pubs_list = order_pubs_by_property(pubs, 'saved_count')
		for pub in savest_pubs_list:
			if pub.author: # ибо есть возможность сохранения публикаций на случай удаления их автора по какой-либо причине 
				if not first_author:
					first_author = pub.author
				if first_author and pub.author != first_author and not second_author:
					second_author = pub.author
				if second_author and not third_author and not pub.author.id in [first_author.id, second_author.id]:
					third_author = pub.author
				if second_author and third_author:
					break

	content = {
        'saved_pubs_count': saved_pubs_count,
        'first_author': first_author,
        'second_author': second_author,
        'third_author': third_author,
		}

	print(content)
	return render(request, 'mainapp/index.html', content)
