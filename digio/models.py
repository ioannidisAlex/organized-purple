import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Tag(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=150, null=True)

	def __str__(self):
		return self.name

class Manager(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=30)

class Program(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	address = models.IntegerField()
	title = models.CharField(max_length=50)


class ProjectnGrant(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	grant = models.IntegerField()
	general_program = models.ForeignKey(
		Program, models.SET_NULL, blank=True, null=T)
	#another entity for many to many
	#so that for every connection there is one
	#connection with a new class object connection
	tags = models.ManyToManyField(Tag)
	#duration = models.DurationField()
	start_time = models.DateTimeField(null=False)
	end_time = models.DateTimeField(null=False)

	duration = models.IntegerField()

	summary = models.CharField(max_length = 3000)

	def save(self, *args, **kwargs):
		self.duration = (self.end_time - self.start_time).days//360
		super(ProjectnGrant, self).save(*args, **kwargs)
	
	#def duration(self):
	#	return (self.end_time - self.start_time).days/360

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

class Organization(models.Model):
	ORGANIZATION_TYPE_CHOISES = [
		(1, "Company"),
		(2, "University"),
		(3, "ResearchCenter"),
	]
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=30)
	abbreviation =  models.CharField(max_length=10)
	phones = models.CharField(max_length=200)
	address = models.CharField(max_length=50)
	zip_code = models.CharField(max_length=7)
	city = models.CharField(max_length=20)
	self_street = models.CharField(max_length=30)
	org_type = models.IntegerField(choises=ORGANIZATION_TYPE_CHOISES)

	is_a = None

	def save(self, *args, **kwargs):
		if(self.org_type == 1):
			self.is_a = Company()
		elif(self.org_type == 2):
			self.is_a = University()
		else:
			self.is_a = ResearchCenter()

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

class WorksAt(models.Model):
	researcher = models.ForeignKey(
		Researcher, on_delete=models.CASCADE
	)

