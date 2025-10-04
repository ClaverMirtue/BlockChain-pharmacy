from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from pharmacyapp.models import Manufacturer, Distributor, Pharmacy, Medicine, SupplyChain
import random

class Command(BaseCommand):
    help = 'Loads initial data for the pharmacy supply chain system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating initial data...')

        # Create Manufacturers
        manufacturers = [
            {
                'name': 'PharmaTech Industries',
                'license_number': 'MAN001',
                'contact_number': '+1-555-0101',
                'email': 'contact@pharmatech.com',
                'address': '123 Pharma Street, Medical City'
            },
            {
                'name': 'MediCorp Solutions',
                'license_number': 'MAN002',
                'contact_number': '+1-555-0102',
                'email': 'info@medicorp.com',
                'address': '456 Health Avenue, Wellness Town'
            },
            {
                'name': 'BioMed Pharmaceuticals',
                'license_number': 'MAN003',
                'contact_number': '+1-555-0103',
                'email': 'support@biomed.com',
                'address': '789 Science Road, Research City'
            }
        ]

        for manufacturer_data in manufacturers:
            Manufacturer.objects.get_or_create(
                license_number=manufacturer_data['license_number'],
                defaults=manufacturer_data
            )

        # Create Distributors
        distributors = [
            {
                'name': 'Global Medical Distributors',
                'license_number': 'DIS001',
                'contact_number': '+1-555-0201',
                'email': 'contact@gmd.com',
                'address': '101 Distribution Center, Logistics City'
            },
            {
                'name': 'HealthCare Logistics',
                'license_number': 'DIS002',
                'contact_number': '+1-555-0202',
                'email': 'info@hcl.com',
                'address': '202 Supply Chain Road, Delivery Town'
            },
            {
                'name': 'MediSupply Solutions',
                'license_number': 'DIS003',
                'contact_number': '+1-555-0203',
                'email': 'support@medisupply.com',
                'address': '303 Warehouse Street, Storage City'
            }
        ]

        for distributor_data in distributors:
            Distributor.objects.get_or_create(
                license_number=distributor_data['license_number'],
                defaults=distributor_data
            )

        # Create Pharmacies
        pharmacies = [
            {
                'name': 'City Health Pharmacy',
                'license_number': 'PHARM001',
                'contact_number': '+1-555-0301',
                'email': 'contact@cityhealth.com',
                'address': '404 Main Street, Downtown'
            },
            {
                'name': 'Community Medical Store',
                'license_number': 'PHARM002',
                'contact_number': '+1-555-0302',
                'email': 'info@communitymed.com',
                'address': '505 Local Road, Neighborhood'
            },
            {
                'name': 'Wellness Pharmacy',
                'license_number': 'PHARM003',
                'contact_number': '+1-555-0303',
                'email': 'support@wellnesspharm.com',
                'address': '606 Health Boulevard, Wellness District'
            }
        ]

        for pharmacy_data in pharmacies:
            Pharmacy.objects.get_or_create(
                license_number=pharmacy_data['license_number'],
                defaults=pharmacy_data
            )

        # Create Medicines
        medicines = [
            {
                'name': 'Paracetamol 500mg',
                'description': 'Pain reliever and fever reducer',
                'price': 5.99,
                'quantity': 1000,
                'batch_number': 'BATCH001',
                'manufacturing_date': timezone.now().date(),
                'expiry_date': timezone.now().date() + timedelta(days=365),
                'manufacturer': Manufacturer.objects.get(license_number='MAN001')
            },
            {
                'name': 'Amoxicillin 250mg',
                'description': 'Antibiotic for bacterial infections',
                'price': 12.99,
                'quantity': 500,
                'batch_number': 'BATCH002',
                'manufacturing_date': timezone.now().date(),
                'expiry_date': timezone.now().date() + timedelta(days=365),
                'manufacturer': Manufacturer.objects.get(license_number='MAN002')
            },
            {
                'name': 'Omeprazole 20mg',
                'description': 'Acid reducer for heartburn',
                'price': 8.99,
                'quantity': 750,
                'batch_number': 'BATCH003',
                'manufacturing_date': timezone.now().date(),
                'expiry_date': timezone.now().date() + timedelta(days=365),
                'manufacturer': Manufacturer.objects.get(license_number='MAN003')
            }
        ]

        for medicine_data in medicines:
            Medicine.objects.get_or_create(
                batch_number=medicine_data['batch_number'],
                defaults=medicine_data
            )

        # Create Supply Chains
        statuses = ['pending', 'in_transit', 'delivered']
        for medicine in Medicine.objects.all():
            for distributor in Distributor.objects.all():
                for pharmacy in Pharmacy.objects.all():
                    SupplyChain.objects.get_or_create(
                        medicine=medicine,
                        manufacturer=medicine.manufacturer,
                        distributor=distributor,
                        pharmacy=pharmacy,
                        defaults={
                            'quantity': random.randint(50, 200),
                            'status': random.choice(statuses)
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Successfully created initial data')) 