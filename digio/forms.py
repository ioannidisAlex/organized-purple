from django.forms import ModelForm
from .models import Program, Tag
from django import forms

class ProgramForm(ModelForm):
	class Meta:
		model = Program
		fields = ['address','title']

class TabsPerSix(forms.Form):
	date_from = forms.CharField(max_length=100)
	date_to = forms.CharField(max_length=100)

class AllOfThem(forms.Form):
	search_date = forms.DateTimeField()
	duration = forms.CharField(required=False)

class ViewProjects(forms.Form):
	id = forms.CharField(max_length=45)

class SelectTag(ModelForm):
	id = forms.CharField(max_length=45)
	class Meta:
		model = Tag
		fields = ['name']