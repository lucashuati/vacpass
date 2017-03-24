from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^vacpass/', include('vacpass.urls')),
    url('^contas/', include('django.contrib.auth.urls')),
    url(r'^$', RedirectView.as_view(url='/vacpass/', permanent=True)),
]
