from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

admin.site.site_header = 'Administraçao VacPass'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^vacpass/', include('vacpass.urls')),
    url('^contas/login/$', auth_views.login, name='login', kwargs={'redirect_authenticated_user': True}),
    url('^contas/', include('django.contrib.auth.urls')),
    url(r'^$', RedirectView.as_view(url='/vacpass/', permanent=True)),
    url(r'^index/$', RedirectView.as_view(url='/vacpass/', permanent=True)),
]
