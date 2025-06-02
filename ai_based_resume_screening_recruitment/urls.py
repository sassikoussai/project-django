from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from screening.schema import schema  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('screening.urls')),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)