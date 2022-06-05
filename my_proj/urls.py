"""my_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import include, path, re_path
from django.utils import timezone

from django.views.generic import TemplateView

from digio import views as common_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", common_views.home, name="home"),
    path("home/", common_views.home, name="home"),
    path('create-program/', common_views.createProgram, name="createProgram"),
    path('generate/', common_views.generate_researchers, name="generate"),
    path('testQuery/', common_views.TestDbCursor.as_view(), name="testQ"),
    path('selectAll/', common_views.AllOfThem.as_view(), name='selectAll'),
    path('searchResearchers/', common_views.IdToResearchers.as_view(), name='showResearchers'),
    path('viewProjects/', common_views.IdToGrants.as_view(), name='viewProjects'),
    path('viewResearcher/', common_views.ResearcherInfo.as_view(), name='viewResearcher'),
    path('perTag/', common_views.TagNGrants.as_view(), name="perTag"),
    path('orgzHaveShame/', common_views.OrganizationSame.as_view(), name="orgzHaveShame"),
    path('topTags/', common_views.TopTags.as_view(),name="topTags"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

