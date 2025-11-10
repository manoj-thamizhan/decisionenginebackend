from rest_framework import serializers
from .models import Rule, UdiFiaWorkflow,  ChangesInvolved, Flow




class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = ("id", "name", "nodes", "edges", "node_id",  "created_at", "updated_at")
        read_only_fields = ("id", "owner", "created_at", "updated_at")

    def validate_nodes(self, value):
        # Basic validation: ensure nodes is a list or dict (tweak as required)
        if not isinstance(value, (list, dict)):
            raise serializers.ValidationError("nodes must be a JSON array or object.")
        return value

    def validate_edges(self, value):
        if not isinstance(value, (list, dict)):
            raise serializers.ValidationError("edges must be a JSON array or object.")
        return value






class UdiFiaWorkflowSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = UdiFiaWorkflow
        # include id so frontend can refer to instances
        fields = [
            'id',
            'health_authority',
            'udi_regulation',
            'category',
            'data_property',
            'data_attribute_ha_field_name',
            'gude_field_name',
            'jnj_udi_data_element',
            'gude_field_number',
            'budi_attribute_eudamed_only',
            'gs1_gtin_trigger_100782299_appendix_b',
            'health_authority_gtin_trigger',
            'jjmt_use_directive',
            'mandatory_field_in_database',
            'field_type',
            'add_flag',
            'edit_flag',
            'delete_flag',
            'change_condition_or_scenarios',
            'additional_change_request_requirements',
            'dri_comments',
            'gtin_outcome_action',
            'data_source_outcome_action',
        ]

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = [
            'id',
            'health_authority',
            'udi_regulation',
            'category',
            'data_property',
            'data_attribute_ha_field_name',
            'gude_field_name',
            'jnj_udi_data_element',
            'gude_field_number',
            'budi_attribute_eudamed_only',
            'gs1_gtin_trigger_100782299_appendix_b',
            'health_authority_gtin_trigger',
            'jjmt_use_directive',
            'mandatory_field_in_database',
            'field_type',
            'add_flag',
            'edit_flag',
            'delete_flag',
            'change_condition_or_scenarios',
            'additional_change_request_requirements',
            'dri_comments',
            'gtin_outcome_action',
            'data_source_outcome_action',
        ]

class ChangesInvolvedSerializer(serializers.ModelSerializer):


    class Meta:
        model = ChangesInvolved
        fields = [
            'workflow',
            'change_category',
            'change_description',
        ]
