from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mysite.views.home_view import Home
from mysite.views.generate_pdf_view import GeneratePDFForm


urlpatterns = [
    path('', Home.as_view(), name='home'),

    # FOR PHOTOS
    path('admin/', admin.site.urls),

    # ONLY FOR CREATING PDF
    path('upload_photo_without_DB/',    GeneratePDFForm.as_view(), name='upload_photo_without_DB'),
]

# tylko do developmentu
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
