"""
URL configuration for ounje project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# schema_view = get_swagger_view(title='Ọ̀unje API')
schema_view = get_schema_view(
   openapi.Info(
      title="Ọ̀unje API",
      default_version='v1',
      description="Ọ̀unje, the culinary wizard, the food plan generator extraordinaire! 🧙‍♂️✨ With a few clicks and some digital sorcery, Ọ̀unje conjures up delightful food plans for your day, for as many days as you desire. 🌮🍳🥗 Breakfast, lunch, and dinner will dance together in perfect harmony. It's like having a personal chef, but without the messy kitchen! 🎩🍽️",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="lawalafeez052@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/v1/', include('api.urls')),
    # path('api/v1/docs', SchemaView.as_view()),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
