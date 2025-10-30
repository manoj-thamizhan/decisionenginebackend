from django.db import models

# Create your models here.

class UdiFiaWorkflow(models.Model):
    change_number = models.CharField(max_length=50)
    udr_fia_number = models.CharField(max_length=50)
    title = models.CharField(max_length=50 ,null=True,blank=True)
    region = models.CharField(max_length=50,null=True,blank=True)
    gtin_change = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_type = models.CharField(max_length=50,null=True,blank=True)
    product_category_unit = models.CharField(max_length=50,null=True,blank=True)
    product_category_level = models.CharField(max_length=50,null=True,blank=True)
    gtin_evaluation =  models.BooleanField(null=True)
    has_udi_health_impact = models.CharField(max_length=5,null=True,blank=True)
    has_impact_in_new_gtin = models.CharField(max_length=5,null=True,blank=True)




# class ChangeCategories(models.Model):
#     name = models.CharField(max_length=50)
#     image = models.ImageField()

class ChangesInvolved(models.Model):
    workflow = models.ForeignKey(UdiFiaWorkflow, on_delete=models.CASCADE)
    change_category = models.CharField(max_length=60)
    # change_category = models.ForeignKey(ChangeCategories, on_delete=models.SET_NULL,null=True)
    change_description = models.TextField(blank=True, null=True)