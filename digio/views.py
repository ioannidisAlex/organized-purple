from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from django.db import transaction
from .models import Program, ProjectnGrant, Researcher, Organization

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
		for i in range(61):
			p = Program(title=f"Post{i}", address=i)
			p.save()
	return redirect('home')

def generate_grants(request):
	with transaction.atomic():
		for i in range(11):
			p = ProjectnGrant(grant=150000000, address=i)
			p.save()
	return redirect('home')

def generate_orgs(request):
	with transaction.atomic():
		for i in range(14):
			p = Organization(name="alef", abbreviation="al",
								phones="123456789",address="dikis",
								zip_code="15442", city="Athens",
								self_street="22",org_type=3
			)
			p.save()
	return redirect('home')
def generate_researchers(request):
	with transaction.atomic():
		for i in range(11):
			p = Researcher(
				project=ProjectnGrant.objects.all().last(),
				name = "alexandros",
				surname = "ioannidis",
				birthdate = "2014-02-09",
				gender = 1,
				age = 54,
				works_at=Organization.objects.all().first()
			)
			p.save()
	return redirect('home')