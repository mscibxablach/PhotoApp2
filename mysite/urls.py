from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mysite.core import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),

    # FOR PHOTOS
    # int:pk - primary key of photo
    path('photos/<int:pk>/', views.delete_photo, name='delete_photo'),

    path('admin/', admin.site.urls),

    # ONLY FOR CREATING PDF
    path('upload_photo_without_DB/', views.upload_photo_without_DB, name='upload_photo_without_DB'),
]

# tylko do developmentu
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
