from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlowViewSet, UdiFiaWorkflowViewSet,  ChangesInvolvedViewSet,WorkflowLookupByIdentifier,DistinctOptionsAPIView

router = DefaultRouter()
router.register(r'workflows', UdiFiaWorkflowViewSet, basename='udifiaworkflow')
router.register(r'changes-involved', ChangesInvolvedViewSet, basename='changesinvolved')
router.register(r"flows", FlowViewSet, basename="flow")

urlpatterns = [
    path('api/', include(router.urls)),
    path('data-from-cn/', WorkflowLookupByIdentifier.as_view()),
    path('options/<int:pk>', DistinctOptionsAPIView.as_view()),
]
