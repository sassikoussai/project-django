from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from screening.schema import schema  
from screening.views import trigger_flyio_deploy  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('screening.urls')),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)), 
    path('trigger_flyio_deploy/', trigger_flyio_deploy, name='trigger_flyio_deploy') 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)