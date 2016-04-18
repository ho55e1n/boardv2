from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  # Examples:
                  # url(r'^$', 'theboard.views.home', name='home'),
                  # url(r'^blog/', include('blog.urls')),

                  url(r'^$', 'boardapp.views.upload_album', name='index'),
                  url(r'^accounts/', include('registration.backends.default.urls')),
                  url(r'^admin/', include(admin.site.urls)),
                  url('', include('social.apps.django_app.urls', namespace='social')),
                  url(r'^upload-media/', 'boardapp.views.upload_media', name='upload'),
                  url(r'^sort/', 'boardapp.views.sort', name='sort'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
