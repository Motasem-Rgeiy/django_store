from django.contrib import admin
from . import  models
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 20
    
@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_per_page = 20

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 20

@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_per_page = 20

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_select_related = ['transaction'] #Always set the relation for best DB fetching practice 
    list_display = ['id' , 'email' , 'amount' , 'payment_method' , 'items' , 'created_at'] #These fields is came from "Transaction"

    #Helper methods
    def amount(self , obj):
        #to check if an order has a transaction (may be some of them does not have for testing reasons)
        if obj.transaction:
            return obj.transaction.amount
        return '-'
    

    def items(self , obj):
        if obj.transaction and obj.transaction.items:
            return len(obj.transaction.items)
        return '-'
    
    def email(self , obj):
        if obj.transaction:
            return obj.transaction.customer_email
        return '-'

    
    def payment_method(self , obj):
        #to check if an order has a transaction (may be some of them does not have for testing reasons)
        if obj.transaction:
            return obj.transaction.get_payment_method_display()
        return '-'
    
    


    #This method to prevent the admin to edit the order
    def has_change_permission(self, request, obj = None):
        return False 
    
    def has_add_permission(self, request , obj=None):
        return False
    
#To change the form style of the admin "order" page, create> templates/admin/appName/modelName/change_form.html
#You have "original" name as a the object name which is "order" inside the template "change_form.html"