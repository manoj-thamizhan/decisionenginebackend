from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend  # optional, if you have django-filter
from .models import UdiFiaWorkflow,  ChangesInvolved
from .serializers import (
    UdiFiaWorkflowSerializer,
    ChangesInvolvedSerializer
)

class UdiFiaWorkflowViewSet(viewsets.ModelViewSet):
    queryset = UdiFiaWorkflow.objects.all().order_by('-created_at')
    serializer_class = UdiFiaWorkflowSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region', 'product_type', 'product_category_unit', 'product_category_level', 'gtin_change']
    search_fields = ['title', 'change_number', 'udr_fia_number']
    ordering_fields = ['created_at', 'updated_at', 'title']


# class ChangeCategoriesViewSet(viewsets.ModelViewSet):
#     queryset = ChangeCategories.objects.all().order_by('name')
#     serializer_class = ChangeCategoriesSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['name']
#     ordering_fields = ['name']


class ChangesInvolvedViewSet(viewsets.ModelViewSet):
    queryset = ChangesInvolved.objects.select_related('workflow', 'change_category').all().order_by('-id')
    serializer_class = ChangesInvolvedSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['workflow', 'change_category']
    search_fields = ['change_description']
    ordering_fields = ['id']
