from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.gis import admin
from django.views.generic import TemplateView
import venues.urls
import venues.views as views


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^restaurants/', include(venues.urls)),

    url(r'^moderate-reports/$', views.moderate_reports),
    url(r'^reports/(?P<pk>[0-9]+)/moderate/$', views.moderate_report),

    #python-social-login urls
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^register-by-token/(?P<backend>[^/]+)/$', views.register_by_access_token),

    # pinax accounts urls
    url(r"^owner/$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^owner/account/", include("account.urls")),

    url(r'^logout/$', 'restaurant.views.logout_view'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.closest),

    # url(r'^logout/$', views.log_out),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns