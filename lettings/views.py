from django.shortcuts import render

from lettings.models import Letting

# Create your views here.
# Aenean leo magna, vestibulum et tincidunt fermentum, consectetur quis velit.
# Sed non placerat massa.
# Integer est nunc, pulvinar a tempor et, bibendum id arcu. Vestibulum ante
# ipsum primis in faucibus orciluctus et ultrices posuere cubilia curae;
# Cras eget scelerisque


def index(request):
    lettings_list = Letting.objects.all()
    context = {"lettings_list": lettings_list}
    return render(request, "lettings/index.html", context)
