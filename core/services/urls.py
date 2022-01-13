from django.urls import include, path, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

# URL patterns for ViewSets are added via rest_framework.routers.SimpleRouter
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
# Hide root view for /api
router.include_root_view = False

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
app_name = 'services'
urlpatterns = [
    path('', include(router.urls)),
    path('sample/', views.SampleAPI1.as_view()),
    re_path(r'^docs(?P<format>\.json|\.yaml)$', views.SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', views.SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]