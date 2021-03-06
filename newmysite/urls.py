from django.conf.urls import patterns, include, url
from django.contrib import admin
from newmysite.views import *

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'newmysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', start),
    url(r'^admin/', include(admin.site.urls)),
    url('^encryption/$', encrypt),
    url('^decryption/$', dencrypt),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
