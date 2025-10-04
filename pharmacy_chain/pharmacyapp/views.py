from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth import login
from .models import Manufacturer, Distributor, Pharmacy, Medicine, SupplyChain, Transaction
from .forms import CustomSignUpForm
from web3 import Web3
import json

# Initialize Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Local Ganache instance

def home(request):
    # Get some statistics for the home page
    stats = {
        'total_medicines': Medicine.objects.count(),
        'total_manufacturers': Manufacturer.objects.count(),
        'total_distributors': Distributor.objects.count(),
        'total_pharmacies': Pharmacy.objects.count(),
        'active_supply_chains': SupplyChain.objects.filter(status__in=['pending', 'in_transit']).count(),
        'completed_deliveries': SupplyChain.objects.filter(status='delivered').count()
    }
    return render(request, 'pharmacyapp/home.html', {'stats': stats})

def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create corresponding profile based on role
            role = form.cleaned_data.get('role')
            if role == 'manufacturer':
                Manufacturer.objects.create(
                    name=f"{user.first_name} {user.last_name}",
                    email=user.email,
                    license_number=f"MAN{user.id:04d}",
                    contact_number="",
                    address=""
                )
            elif role == 'distributor':
                Distributor.objects.create(
                    name=f"{user.first_name} {user.last_name}",
                    email=user.email,
                    license_number=f"DIS{user.id:04d}",
                    contact_number="",
                    address=""
                )
            elif role == 'pharmacy':
                Pharmacy.objects.create(
                    name=f"{user.first_name} {user.last_name}",
                    email=user.email,
                    license_number=f"PHARM{user.id:04d}",
                    contact_number="",
                    address=""
                )
            
            login(request, user)
            messages.success(request, 'Account created successfully! Please complete your profile.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomSignUpForm()
    return render(request, 'pharmacyapp/signup.html', {'form': form})

@login_required
def dashboard(request):
    supply_chains = SupplyChain.objects.all().order_by('-created_at')
    
    # Get counts for each status
    status_counts = SupplyChain.objects.values('status').annotate(count=Count('id'))
    counts = {
        'total': supply_chains.count(),
        'delivered': 0,
        'in_transit': 0,
        'pending': 0
    }
    
    for status in status_counts:
        counts[status['status']] = status['count']
    
    return render(request, 'pharmacyapp/dashboard.html', {
        'supply_chains': supply_chains,
        'counts': counts
    })

@login_required
def create_supply_chain(request):
    if request.method == 'POST':
        medicine_id = request.POST.get('medicine')
        manufacturer_id = request.POST.get('manufacturer')
        distributor_id = request.POST.get('distributor')
        pharmacy_id = request.POST.get('pharmacy')
        quantity = request.POST.get('quantity')

        try:
            supply_chain = SupplyChain.objects.create(
                medicine_id=medicine_id,
                manufacturer_id=manufacturer_id,
                distributor_id=distributor_id,
                pharmacy_id=pharmacy_id,
                quantity=quantity
            )
            
            # Deploy smart contract
            contract_address = deploy_smart_contract(supply_chain)
            supply_chain.smart_contract_address = contract_address
            supply_chain.save()
            
            messages.success(request, 'Supply chain created successfully!')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Error creating supply chain: {str(e)}')
    
    medicines = Medicine.objects.all()
    manufacturers = Manufacturer.objects.all()
    distributors = Distributor.objects.all()
    pharmacies = Pharmacy.objects.all()
    
    return render(request, 'pharmacyapp/create_supply_chain.html', {
        'medicines': medicines,
        'manufacturers': manufacturers,
        'distributors': distributors,
        'pharmacies': pharmacies
    })

@login_required
def update_supply_chain_status(request, pk):
    supply_chain = get_object_or_404(SupplyChain, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        try:
            supply_chain.status = new_status
            supply_chain.save()
            
            # Update smart contract
            update_smart_contract_status(supply_chain.smart_contract_address, new_status)
            
            messages.success(request, 'Status updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating status: {str(e)}')
    
    return redirect('dashboard')

def deploy_smart_contract(supply_chain):
    # Load contract ABI and bytecode
    with open('pharmacyapp/contracts/SupplyChain.json', 'r') as f:
        contract_data = json.load(f)
    
    # Deploy contract
    contract = w3.eth.contract(abi=contract_data['abi'], bytecode=contract_data['bytecode'])
    tx_hash = contract.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_receipt.contractAddress

def update_smart_contract_status(contract_address, new_status):
    # Load contract ABI
    with open('pharmacyapp/contracts/SupplyChain.json', 'r') as f:
        contract_data = json.load(f)
    
    # Get contract instance
    contract = w3.eth.contract(address=contract_address, abi=contract_data['abi'])
    
    # Update status
    tx_hash = contract.functions.updateStatus(new_status).transact()
    w3.eth.wait_for_transaction_receipt(tx_hash)

@login_required
def profile(request):
    return redirect('home')
