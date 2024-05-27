from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    sales_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=50)
    sales_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return self.name

class SalesRecord(models.Model):
    date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sales_amount = models.DecimalField(max_digits=10, decimal_places=2)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    receipt_photo = models.ImageField(upload_to='receipts/')

    def __str__(self):
        return f"{self.product} sold in {self.region} on {self.date} for {self.sales_amount}"
    

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             # New instance
#             region_obj = self.region
#             product_obj =self.product

# # Retrieve the current sales_amount value from the database
#             current_sales_amount = region_obj.sales_amount
#             pc = product_obj.sales_amount

# # Perform the addition operation in Python
#             new_sales_amount = current_sales_amount + self.sales_amount
#             npc = pc + self.sales_amount

# # Update the sales_amount field with the new value
#             region_obj.sales_amount = new_sales_amount
#             product_obj.sales_amount =  npc
# # Save the updated region object back to the database
            
#         else:
#             # Existing instance
#             old_record = SalesRecord.objects.get(pk=self.pk)
#             # Fetch the region object
#             region_obj = self.region
#             product_obj =self.product

#             # Retrieve the current sales_amount value from the database
#             current_sales_amount = region_obj.sales_amount
#             pc = product_obj.sales_amount

#             # Calculate the new sales_amount value
#             new_sales_amount = current_sales_amount - old_record.sales_amount + self.sales_amount
#             npc = pc + self.sales_amount - old_record.sales_amount

#             # Update the sales_amount field with the new value
#             region_obj.sales_amount = new_sales_amount
#             product_obj.sales_amount = npc

#             # Save the updated region object back to the database
#         # self.region.save(update_fields =['sales_amount'])

#         super().save(*args, **kwargs)

#     # def delete(self, *args, **kwargs):
#     #     self.region.sales_amount = F('sales_amount') - self.sales_amount
#     #     self.region.save(update_fields=['sales_amount'])
#     #     super().delete(*args, **kwargs)
