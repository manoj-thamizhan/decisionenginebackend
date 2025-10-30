from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UdiFiaWorkflowViewSet,  ChangesInvolvedViewSet

router = DefaultRouter()
router.register(r'workflows', UdiFiaWorkflowViewSet, basename='udifiaworkflow')
# router.register(r'change-categories', ChangeCategoriesViewSet, basename='changecategories')
router.register(r'changes-involved', ChangesInvolvedViewSet, basename='changesinvolved')

urlpatterns = [
    path('api/', include(router.urls)),
]
