import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Tag(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=150, null=True)

	def __str__(self):
		return self.name
