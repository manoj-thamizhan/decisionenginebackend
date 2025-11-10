from django.db import models

# Create your models here.

class UdiFiaWorkflow(models.Model):
    health_authority = models.CharField(max_length=100, null=True, blank=True)
    udi_regulation = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    data_property = models.CharField(max_length=100, null=True, blank=True)
    data_attribute_ha_field_name = models.CharField(max_length=150, null=True, blank=True)
    gude_field_name = models.CharField(max_length=150, null=True, blank=True)
    jnj_udi_data_element = models.CharField(max_length=150, null=True, blank=True)
    gude_field_number = models.CharField(max_length=50, null=True, blank=True)
    budi_attribute_eudamed_only = models.CharField(max_length=150, null=True, blank=True)
    gs1_gtin_trigger_100782299_appendix_b = models.CharField(max_length=150, null=True, blank=True)
    health_authority_gtin_trigger = models.CharField(max_length=150, null=True, blank=True)
    jjmt_use_directive = models.CharField(max_length=100, null=True, blank=True)
    mandatory_field_in_database = models.CharField(max_length=10, null=True, blank=True)
    field_type = models.CharField(max_length=50, null=True, blank=True)
    add_flag = models.CharField(max_length=10, null=True, blank=True)
    edit_flag = models.CharField(max_length=10, null=True, blank=True)
    delete_flag = models.CharField(max_length=10, null=True, blank=True)
    change_condition_or_scenarios = models.TextField(null=True, blank=True)
    additional_change_request_requirements = models.TextField(null=True, blank=True)
    dri_comments = models.TextField(null=True, blank=True)
    gtin_outcome_action = models.CharField(max_length=100, null=True, blank=True)
    data_source_outcome_action = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Flow(models.Model):
    """
    Stores a React Flow diagram.
    - name: human readable name
    - nodes: JSON representation of nodes (array/object depending on your frontend)
    - edges: JSON representation of edges
    - node_id: an optional "current node id" or metadata from frontend
    - owner: optional FK to user (nullable) — remove if not needed
    """
    name = models.CharField(max_length=255)
    nodes = models.JSONField()
    edges = models.JSONField()
    node_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)

    def __str__(self):
        return f"{self.name} ({self.id})"


class Rule(models.Model):
    health_authority = models.CharField(max_length=100, null=True, blank=True)
    udi_regulation = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    data_property = models.CharField(max_length=100, null=True, blank=True)
    data_attribute_ha_field_name = models.CharField(max_length=150, null=True, blank=True)
    gude_field_name = models.CharField(max_length=150, null=True, blank=True)
    jnj_udi_data_element = models.CharField(max_length=150, null=True, blank=True)
    gude_field_number = models.CharField(max_length=50, null=True, blank=True)
    budi_attribute_eudamed_only = models.CharField(max_length=150, null=True, blank=True)
    gs1_gtin_trigger_100782299_appendix_b = models.CharField(max_length=150, null=True, blank=True)
    health_authority_gtin_trigger = models.CharField(max_length=150, null=True, blank=True)
    jjmt_use_directive = models.CharField(max_length=100, null=True, blank=True)
    mandatory_field_in_database = models.CharField(max_length=10, null=True, blank=True)
    field_type = models.CharField(max_length=50, null=True, blank=True)
    add_flag = models.CharField(max_length=10, null=True, blank=True)
    edit_flag = models.CharField(max_length=10, null=True, blank=True)
    delete_flag = models.CharField(max_length=10, null=True, blank=True)
    change_condition_or_scenarios = models.TextField(null=True, blank=True)
    additional_change_request_requirements = models.TextField(null=True, blank=True)
    dri_comments = models.TextField(null=True, blank=True)
    gtin_outcome_action = models.CharField(max_length=100, null=True, blank=True)
    data_source_outcome_action = models.CharField(max_length=100, null=True, blank=True)



    def __str__(self):
        return f"{self.health_authority or 'Rule'} - {self.udi_regulation or ''}"

# class ChangeCategories(models.Model):
#     name = models.CharField(max_length=50)
#     image = models.ImageField()

class ChangesInvolved(models.Model):
    workflow = models.ForeignKey(UdiFiaWorkflow, on_delete=models.CASCADE)
    change_category = models.CharField(max_length=60)
    # change_category = models.ForeignKey(ChangeCategories, on_delete=models.SET_NULL,null=True)
    change_description = models.TextField(blank=True, null=True)


class PLMWindchillMockdata(models.Model):
    change_number = models.CharField(max_length=30)
    udi_fia_number = models.CharField(max_length=30)
    data = models.TextField()