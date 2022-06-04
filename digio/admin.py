from django.contrib import admin
from digio.models import Manager, Organization, ResearchCenter, University, Company, Program, ProjectnGrant, Tag, Assessment, Delivery, Researcher
# Register your models here.

admin.site.register(Manager)
admin.site.register(ResearchCenter)
admin.site.register(University)
admin.site.register(Company)
admin.site.register(Organization)
admin.site.register(ProjectnGrant)
admin.site.register(Program)
admin.site.register(Tag)
admin.site.register(Assessment)
admin.site.register(Delivery)
admin.site.register(Researcher)