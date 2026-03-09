import { Component, OnInit } from '@angular/core';
import { CustomerService, Customer } from '../../services/customer.service';

@Component({
  selector: 'app-customers',
  templateUrl: './customers.component.html'
})
export class CustomersComponent implements OnInit {
  customers: Customer[] = [];
  searchQuery = '';
  showAddForm = false;
  isEditing = false;
  currentCustomer: Customer = this.getEmptyCustomer();

  constructor(private customerService: CustomerService) { }

  ngOnInit() {
    this.loadCustomers();
  }

  getEmptyCustomer(): Customer {
    return { name: '', phone: '', email: '', address: '', customer_type: 'Individual' };
  }

  loadCustomers() {
    this.customerService.getCustomers(this.searchQuery).subscribe(data => this.customers = data);
  }

  onSearch() {
    this.loadCustomers();
  }

  onSubmit() {
    if (this.isEditing && this.currentCustomer.id) {
      this.customerService.updateCustomer(this.currentCustomer.id, this.currentCustomer).subscribe(() => {
        this.resetForm();
        this.loadCustomers();
      });
    } else {
      this.customerService.createCustomer(this.currentCustomer).subscribe(() => {
        this.resetForm();
        this.loadCustomers();
      });
    }
  }

  editCustomer(c: Customer) {
    this.currentCustomer = { ...c };
    this.isEditing = true;
    this.showAddForm = true;
  }

  deleteCustomer(id: number) {
    if (confirm('Are you sure you want to delete this customer?')) {
      this.customerService.deleteCustomer(id).subscribe(() => this.loadCustomers());
    }
  }

  resetForm() {
    this.currentCustomer = this.getEmptyCustomer();
    this.isEditing = false;
    this.showAddForm = false;
  }
}
