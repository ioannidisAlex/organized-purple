from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from django.db import transaction
from .models import Program
from .forms import ProgramForm

def home(request):
    return render(request, "home.html")

def createProgram(request):
	form = ProgramForm()

	if request.method == 'POST':
		#print('FORM DATA:', request.POST)
		form = ProgramForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')

	context = {'form': form}
	return render(request, 'program-form.html', context)

def generate_objects(request):
	with transaction.atomic():
		for i in range(11):
			p = Post(title=f"Post{i}")
			p.save()
	redirect('home')