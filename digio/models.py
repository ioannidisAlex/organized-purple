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
	title = models.CharField(max_length=50)
	manager = models.ForeignKey(
		Manager, on_delete = models.CASCADE
	)

class ProjectnGrant(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	grant = models.IntegerField()
	general_program = models.ForeignKey(
		Program, models.SET_NULL, blank=True, null=True
	)
	#another entity for many to many
	#so that for every connection there is one
	#connection with a new class object connection
	tags = models.ManyToManyField(Tag)
	#duration = models.DurationField()
	start_time = models.DateTimeField(null=False)
	end_time = models.DateTimeField(null=False)
	
	def duration(self):
		return self.end_time - self.start_time