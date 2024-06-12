from .models import *


def menu_links(request):
    links = Category.objects.all()
    return {'links': links}