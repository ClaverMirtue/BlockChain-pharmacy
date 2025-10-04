from django.contrib import admin
from .models import Manufacturer, Distributor, Pharmacy, Medicine, SupplyChain, Transaction

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number', 'contact_number', 'email', 'created_at')
    search_fields = ('name', 'license_number', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number', 'contact_number', 'email', 'created_at')
    search_fields = ('name', 'license_number', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number', 'contact_number', 'email', 'created_at')
    search_fields = ('name', 'license_number', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'price', 'quantity', 'batch_number', 'manufacturing_date', 'expiry_date')
    search_fields = ('name', 'batch_number')
    list_filter = ('manufacturer', 'manufacturing_date', 'expiry_date')
    ordering = ('-created_at',)
    date_hierarchy = 'manufacturing_date'

@admin.register(SupplyChain)
class SupplyChainAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'manufacturer', 'distributor', 'pharmacy', 'quantity', 'status', 'created_at')
    search_fields = ('medicine__name', 'manufacturer__name', 'distributor__name', 'pharmacy__name')
    list_filter = ('status', 'created_at', 'manufacturer', 'distributor', 'pharmacy')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('supply_chain', 'transaction_hash', 'from_address', 'to_address', 'amount', 'created_at')
    search_fields = ('transaction_hash', 'from_address', 'to_address')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
