from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    context = {}
    return render(request, 'refts_json_compiler/home.html', context)
