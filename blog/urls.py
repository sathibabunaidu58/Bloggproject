from django.urls import path
from .views import *


urlpatterns = [
    path('',home,name='home'),
    path('sign-up/',signup_form,name='sign'),
    path('login/',login_form,name='login'),
    path('room/<str:pk>/',room_page,name='room_page'),
    path('logout/',logout_user,name='logout'),
    path('ebit/<str:pk>/',edit,name='edit'),
    path('delete/<str:pk>/',delete_post,name='delete'),
    path('create',create_post,name='create'),
    path('profile/<str:pk>',profile,name='profile'),
]



from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


