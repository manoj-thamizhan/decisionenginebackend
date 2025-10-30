from rest_framework import serializers
from .models import UdiFiaWorkflow,  ChangesInvolved

# class ChangeCategoriesSerializer(serializers.ModelSerializer):
#     image = serializers.ImageField(required=False, allow_null=True)

#     class Meta:
#         model = ChangeCategories
#         fields = ['id', 'name', 'image']


class UdiFiaWorkflowSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UdiFiaWorkflow
        # include id so frontend can refer to instances
        fields = [
            'id',
            'change_number',
            'udr_fia_number',
            'title',
            'region',
            'gtin_change',
            'created_at',
            'updated_at',
            'product_type',
            'product_category_unit',
            'product_category_level',
            'gtin_evaluation',
            'has_udi_health_impact',
            'has_impact_in_new_gtin',
        ]


class ChangesInvolvedSerializer(serializers.ModelSerializer):


    class Meta:
        model = ChangesInvolved
        fields = [
            'workflow',
            'change_category',
            'change_description',
        ]
