
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from clinic_management import views, admin_views
from config import settings


urlpatterns = [
    path('demo/', views.showDemoPage),
    path('', views.showLoginPage),
    path('get_user_details', views.getUserDetails),
    path('logout_user', views.logoutUser),
    path('admin/', admin.site.urls),
    path('doLogin', views.doLogin),
    path('admin_home/', admin_views.admin_home),
    path('add_doctor/', admin_views.add_doctor),
    path('add_doctor_save/', admin_views.add_doctor_save)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
