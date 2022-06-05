from collections import namedtuple

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.db import connections
from django.utils.decorators import method_decorator
from django.views import View

from collections import defaultdict

from django.db import transaction
from .models import Program, ProjectnGrant, Researcher, Organization

from .forms import (
	ProgramForm,
	TabsPerSix,
	AllOfThem,
	ViewProjects,
	SelectTag,
)

import datetime
import json 
import logging
logging.basicConfig(level=logging.INFO)
import collections

cursor = connections['default'].cursor()

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class AllOfThem(View):
	template_name = "all.html"
	form_class = AllOfThem

	def get(self, request, *args, **kwargs):
		query = """ SELECT *
					FROM digio_program
		"""
		cursor.execute(query)
		lst = dictfetchall(cursor)
		data = [
			{
				"x" : researcher_index,
				"all" : s
			}
    		for researcher_index, s in enumerate(lst)
		]
		context = {
			"data" : data,
			"form" : self.form_class()
		}
		return render(request, 'date-duration.html', context)	

	def post(self, request, *args, **kwargs):
		date = request.POST["search_date"]
		duration = request.POST['duration']
		print(duration)
		if (duration == ""):
			ts = datetime.datetime(int(date[0:4]), 6, int(date[7:9]))
			#print(ts)
			query = """ SELECT id,summary FROM digio_projectngrant
					WHERE %s BETWEEN digio_projectngrant.start_time AND digio_projectngrant.end_time;
			"""
			cursor.execute(query,(ts,))
		else:
			query = """ SELECT id,summary FROM digio_projectngrant
					WHERE %s = digio_projectngrant.duration;
			"""
			cursor.execute(query,(duration,))
		lst = dictfetchall(cursor)
		data = [
			{
				"x" : grant_index,
				"all" : s
			}
    		for grant_index, s in enumerate(lst)
		]
		context = {
			"data" : data
		}
		return render(request, 'allGrants.html', context)

class IdToResearchers(View):
	template_name = "show_researchers.html"

	def get(self, request, *args, **kwargs):
		print(request)
		return render(request, self.template_name, {})

	def post(self, request, *args, **kwargs):
		id = request.POST["id"]
		#query = """ SELECT id, surname FROM digio_researcher WHERE digio_researcher.project_id = %s;"""
		query = """ SELECT digio_researcher.id 
					FROM digio_researcher 
					INNER JOIN digio_researcher_project 
					ON digio_researcher.id = digio_researcher_project.researcher_id 
					WHERE digio_researcher_project.projectngrant_id = %s """
		cursor.execute(query,(id,))
		lst = dictfetchall(cursor)
		data = [
			{
				"x" : researcher_index,
				"all" : s
			}
    		for researcher_index, s in enumerate(lst)
		]
		context = {
			"data" : data
		}
		return render(request, self.template_name, context)

class IdToProjects(View):
	template_name = "show_grants.html"

	def get(self, request, *args, **kwargs):
		query = """ CREATE VIEW asd
					SELECT *
					FROM digio_researcher_project 
					INNER JOIN digio_projectngrant as t
					ON digio_projectngrant.id = digio_researcher_project.projectngrant_id 
		"""

class IdToGrants(View):
	template_name = "show_grants.html"
	form_class = ViewProjects

	def get(self, request, *args, **kwargs):
		query = """ SELECT *FROM digio_researcher JOIN digio_researcher_project 
					ON digio_researcher.id = digio_researcher_project.researcher_id;
		"""
		cursor.execute(query)
		lst = dictfetchall(cursor)
		data = [
			{
				"x" : grant,
				"all" : s
			}
    		for grant, s in enumerate(lst)
		]
		context = {
			"data" : data,
			"form" : self.form_class()
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		id = request.POST["id"]
		#query = """ SELECT id, surname FROM digio_researcher WHERE digio_researcher.project_id = %s;"""
		query = """ SELECT digio_researcher_project.projectngrant_id
					FROM digio_researcher_project 
					INNER JOIN digio_projectngrant
					ON digio_projectngrant.id = digio_researcher_project.projectngrant_id 
					WHERE digio_researcher_project.researcher_id = %s """
		cursor.execute(query,(id,))
		lst = dictfetchall(cursor)
		data = [
			{
				"x" : researcher_index,
				"all" : s
			}
    		for researcher_index, s in enumerate(lst)
		]
		context = {
			"data" : data
		}
		return render(request, 'show_grants.html', context)

class ResearcherInfo(View):
	template_name = "show_info.html"
	form_class = ViewProjects

	def get(self, request, *args, **kwargs):
		query = """ SELECT *FROM digio_researcher JOIN digio_researcher_project 
					ON digio_researcher.id = digio_researcher_project.researcher_id;
		"""
		cursor.execute(query)
		lst = dictfetchall(cursor)
		data = [
			{
				"x" : grant,
				"all" : s
			}
    		for grant, s in enumerate(lst)
		]
		context = {
			"data" : data,
			"form" : self.form_class()
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		id = request.POST["id"]
		#query = """ SELECT id, surname FROM digio_researcher WHERE digio_researcher.project_id = %s;"""
		query = """ SELECT name, surname, gender
					FROM digio_researcher
					WHERE digio_researcher.id = %s """
		cursor.execute(query,(id,))
		lst = dictfetchall(cursor)
		data = [
			{
				"x" : researcher_index,
				"all" : s
			}
    		for researcher_index, s in enumerate(lst)
		]
		context = {
			"data" : data
		}
		return render(request, 'show_info.html', context)

class TagNGrants(View):
	template_name = "select_tag.html"
	form_class = SelectTag

	def get(self, request, *args, **kwargs):
		query = """ SELECT * FROM digio_tag;
		"""
		cursor.execute(query)
		lst = dictfetchall(cursor)
		data = [
			{
				"x" : grant,
				"all" : s
			}
    		for grant, s in enumerate(lst)
		]
		context = {
			"data" : data,
			"form" : self.form_class()
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		id = request.POST["id"]
		# subquery = 					SELECT * FROM digio_researcher, digio_projectngrant WHERE (digio_projectngrant.id, digio_projectngrant.grant, digio_projectngrant.end_time, digio_projectngrant.general_program_id )= ANY (
		#           CREATE OR REPLACE VIEW grants AS
		query = """ 
					
					SELECT *
					FROM digio_projectngrant 
					WHERE digio_projectngrant.id in (SELECT digio_projectngrant_tags.projectngrant_id
								FROM digio_projectngrant_tags
								WHERE tag_id = %s
										) AND 
								(CURRENT_TIMESTAMP BETWEEN 
								digio_projectngrant.start_time AND 
								digio_projectngrant.end_time); 
				"""
					#Go
					#SELECT *FROM (digio_researcher JOIN digio_researcher_project 
					#ON digio_researcher.id = digio_researcher_project.researcher_id;
					#) as t JOIN digio_projectngrant
					#ON digio_projectngrant.id = t.id 
					#WHERE digio_projectngrant.id = ANY grants.id

					#Go
		cursor.execute(query,(id,))
		lst = dictfetchall(cursor)
		data = [
			{
				"x" : researcher_index,
				"all" : s
			}
    		for researcher_index, s in enumerate(lst)
		]
		context = {
			"data" : data
		}
		return render(request, 'select_tag.html', context)

class OrganizationSame(View):
	template_name = "pop.html"

	def get(self, request, *args, **kwargs):
		query = """ SELECT *
					FROM digio_program
		"""
		cursor.execute(query)
		lst = dictfetchall(cursor)
		data = [
			{
				"x" : researcher_index,
				"all" : s
			}
    		for researcher_index, s in enumerate(lst)
		]
		context = {
			"data" : data,
		}
		return render(request, 'pop.html', context)

class TopTags(View):
	template_name = "show_top_tags.html"

	def get(self, request, *args, **kwargs):
		query = """
					SELECT taga.tag_id as tag_id1, tagb.tag_id as tag_id2, count(*) as TOTAL
					from digio_projectngrant_tags taga, digio_projectngrant_tags tagb
					WHERE taga.id <> tagb.id AND taga.projectngrant_id = tagb.projectngrant_id 
					GROUP BY taga.tag_id, tagb.tag_id
					ORDER BY TOTAL DESC
					LIMIT 3
		"""
		cursor.execute(query)
		lst = dictfetchall(cursor)
		data = [
			{
				"x" : researcher_index,
				"all" : s
			}
    		for researcher_index, s in enumerate(lst)
		]
		context = {
			"data" : data
		}
		return render(request, "show_top_tags.html", context)


class TestDbCursor(View):
	template_name = "test.html"
	form_class = TabsPerSix

	def get(self, request, *args, **kwargs):
		context = {'form': self.form_class()}
		return render(request, 'program-form.html', context)	
		
	def post(self, request, *args, **kwargs):
		query = """ SELECT * FROM digio_program 
				WHERE address<=6; """
		cursor.execute(query)
		lst = dictfetchall(cursor)
		#print(lst)		
		#dick = ""
		#dick += "{"
		#for v,k in enumerate(lst):
		#	dick = dick + '"' + str(v) + '"'
		#	dick = dick + ':'
		#	dick = dick + str(k)			
		#	dick = dick + ","
		#dick = dick[:-1]	
		#dick += "}"
		#context = json.loads(dick)
		#new_dict = {}
		#for item in lst:
		#	name = item['name']
		#	new_dict[name] = item
		#context = new_dict
		output = defaultdict(dict)

		for k,i in enumerate(lst):
			l = k
			#for j in lst
			#output[k][lst[i]] = lst[i]
		#context = output
		#print(output)

		#context = dict((key,d[key]) for d in lst for key in d)
		#print(context)
		#context = {"d"+str(v): k for v, k in enumerate(lst)}
		data = [
			{
				"sex" : session_index,
				"all" : s
			}
    		for session_index, s in enumerate(lst)
		]
		#context = {"pullmeout"+str(v): k for v, k in enumerate(lst)}
		context = {'data': data , 'len': l+1}
		print( context )
		print(context)
		#logging.info(context)
		return render(request, self.template_name, context)


def testdb_cursor(request):
	query = """ SELECT * FROM digio_program 
				WHERE address=6; """
	cursor.execute(query)
	results = namedtuplefetchall(cursor)
	return Response(response)


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