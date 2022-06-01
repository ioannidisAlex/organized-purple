import uuid
import datetime
import random

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class Tag(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=150, null=True)

	def __str__(self):
		return self.name

#class Manager(models.Model):
#	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#	name = models.CharField(max_length=30)

class Program(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	address = models.IntegerField(blank=True, null=True)
	title = models.CharField(max_length=50)

class ResearchCenter(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	budget_from_the_ministry_of_education = models.FloatField()
	budget_from_private_actions = models.FloatField()
	#organization = models.ForeignKey(Organization, on_delete = models.CASCADE)

class University(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	budget_from_the_ministry_of_education = models.FloatField()
	#organization = models.ForeignKey(Organization, on_delete = models.CASCADE)

class Company(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	equity_capital = models.FloatField()
	#def __init__(self, id, equity_capital):
	#	if not self.pk:
	#		self.id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	#		self.equity_capital = 1230.12
	#	super(Company, self).save(*args, **kwargs)

class Organization(models.Model):
	ORGANIZATION_TYPE_CHOICES = [
		(1, "Company"),
		(2, "University"),
		(3, "ResearchCenter"),
	]
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=30, default="alefs")
	abbreviation =  models.CharField(max_length=10, default="alefs")
	phones = models.CharField(max_length=200, default="6973975753")
	address = models.CharField(max_length=50, default="call22")
	zip_code = models.CharField(max_length=7, default="15774")
	city = models.CharField(max_length=20, default="Athens")
	self_street = models.CharField(max_length=30, default="12")
	org_type = models.IntegerField(choices=ORGANIZATION_TYPE_CHOICES)

	is_a = None


	def save(self, *args, **kwargs):
		if(self.org_type == 1):
			self.is_a = Company.objects.create(
								equity_capital= 1023.12)
		elif(self.org_type == 2):
			self.is_a = University.objects.create(budget_from_the_ministry_of_education=70000000)
		else:
			self.is_a = ResearchCenter.objects.create(budget_from_private_actions=123000,
														budget_from_the_ministry_of_education=200000)
		super(Organization, self).save(*args, **kwargs)
	#abstract see lass class meta

	def set_phones(self, x):
		self.phones = json.dumps(x)

	def get_phones(self):
		return json.loads(self.phones)

	def set_address(self, zipCode, street, city):
		self.zipCode = zipCode
		self.street = street
		self.city = city
		self.address = json.dumps("["+self.zipCode+self.street+self.city+"]")

	def get_address(self):
		return json.loads(self.address)

	#class Meta:
    #    abstract = True

class ProjectnGrant(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	grant = models.IntegerField(default="10000")
	general_program = models.ForeignKey(
		Program, models.SET_NULL, blank=True, null=True)
	#manager = models.ForeignKey(
	#	Manager, models.SET_NULL, blank=True, null=True)
	#research_manager = models.ForeignKey(
	#	Researcher, models.SET_NULL, blank=True, null=True)
	#another entity for many to many
	#so that for every connection there is one
	#connection with a new class object connection
	tags = models.ManyToManyField(Tag, blank=True)
	#duration = models.DurationField()
	start_time = models.DateTimeField(default=timezone.now(),blank=True)
	end_time = models.DateTimeField(default=(timezone.now() + datetime.timedelta(hours=84400)))

	duration = models.IntegerField(default=555)

	summary = models.CharField(max_length = 3000)

	is_evaluated = models.BooleanField(default=False, editable=False)
	assesment = None
	
	#researchers = []
	deliveries = []

	def save(self, *args, **kwargs):
		self.duration = (self.end_time - self.start_time).days//360
		super(ProjectnGrant, self).save(*args, **kwargs)
	
	#def duration(self):
	#	return (self.end_time - self.start_time).days/360

class Researcher(models.Model):
	GENDER_TYPE_CHOICES = [
        (1, "male"),
        (2, "female"),
        (3, "prefer not to say"),
    ]
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	project = models.ForeignKey(
		ProjectnGrant, on_delete=models.CASCADE
	)
	name = models.CharField(max_length=40)
	surname = models.CharField(max_length=40)
	birthdate = models.DateField()
	gender = models.IntegerField(choices=GENDER_TYPE_CHOICES)

	age = models.IntegerField(default = 550)

	works_at = models.ForeignKey(
		Organization, on_delete=models.CASCADE, default= Organization.objects.first()
	)

class Assessment(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	evaluation = models.IntegerField(default=99)
	date = models.DateTimeField(null = False)
	resercher_who_evaluates = models.ForeignKey(
		Researcher, on_delete=models.CASCADE
	)

class Delivery(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length = 70)
	summary = models.CharField(max_length= 1000)
	project_and_grant = models.ForeignKey(
		ProjectnGrant, on_delete=models.CASCADE
	)

