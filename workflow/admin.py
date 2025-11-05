from django.contrib import admin

from workflow.models import PLMWindchillMockdata, Rule , UdiFiaWorkflow

# Register your models here.
class RuleAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'region',
        'country',
        'gtin_change',
        'product_type',
        'product_category_unit',
        'product_category_level',
        'gtin_evaluation',
        'has_udi_health_impact',
        'has_impact_in_new_gtin',
    ]
    list_display_links = ['pk']
    list_editable = [
        'region',
        'country',
        'gtin_change',
        'product_type',
        'product_category_unit',
        'product_category_level',
        'gtin_evaluation',
        'has_udi_health_impact',
        'has_impact_in_new_gtin',
    ]

admin.site.register(Rule, RuleAdmin)

admin.site.register( UdiFiaWorkflow)
admin.site.register( PLMWindchillMockdata)