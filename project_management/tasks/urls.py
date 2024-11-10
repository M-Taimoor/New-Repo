# tasks/urls.py
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import TaskViewSet

# router = DefaultRouter()
# router.register(r'tasks', TaskViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]



# tasks/urls.py (URL configuration for your 'tasks' app)
# task/urls.py
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from .views import TaskViewSet

# # Define the OpenAPI schema view with explicit template names
# schema_view = get_schema_view(
#     openapi.Info(
#         title="Project Management API",
#         default_version='v1',
#         description="API documentation for the Project Management application",
#         terms_of_service="https://www.ourapp.com/policies/terms/",
#         contact=openapi.Contact(email="contact@ourapp.com"),
#         license=openapi.License(name="Awesome License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
#     template_name='drf-yasg/swagger-ui.html',  # Set the template name for Swagger
#     # template_name='drf-yasg/redoc.html',    # Uncomment this line if you prefer ReDoc
# )

# router = DefaultRouter()
# router.register(r'tasks', TaskViewSet)

# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     # Uncomment the line below if you prefer to use ReDoc instead of Swagger
#     # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]


# task/urls.py
from django.urls import path
from .views import TaskViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Project Management API",
        default_version='v1',
        description="API documentation for the Project Management application",
        # ...
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list'),
    path('tasks/<int:pk>/', TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='task-detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]