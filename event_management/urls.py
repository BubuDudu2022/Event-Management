from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

from .views import dashboard, login_page, logut_page, user_home, ajax_register, ajax_login, user_logout
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # -------------------------
    # USER SIDE (FRONTEND)
    # -------------------------
    #path('', user_home, name='user_home'),          # This will show your user frontend
    path('login/', login_page, name='login'),
    path('logout/', logut_page, name='logout'),

    # -------------------------
    # ADMIN SIDE (BACKEND)
    # -------------------------
    path('admin-panel/', dashboard, name='dashboard'),   # Admin dashboard moved here

    # events urls
    #path('events/', include('events.urls')),
    path('', include('events.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('user/login/', ajax_login, name='login-ajax'),
    path('user/logout/', user_logout, name='logout-ajax'),
    path('register/', ajax_register, name='register'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
