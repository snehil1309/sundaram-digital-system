import { Component, OnInit, ViewChild } from '@angular/core';
import { OrderService, Order } from '../../services/order.service';
import { CustomerService, Customer } from '../../services/customer.service';
import { NgSelectComponent } from '@ng-select/ng-select'; // Import ngSelectComponent for type reference


@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
})
export class OrdersComponent implements OnInit {
  @ViewChild('orderCreateSelect') orderCreateSelect!: NgSelectComponent; // Reference to the ng-select component
  orders: Order[] = [];
  customers: Customer[] = [];
  showCreateForm = false;
  filterCustomerId: number | string = '';

  // Added for UI features
  showAddCustomerForm = false;
  customerSearch = '';
  filteredCustomers: Customer[] = [];

  categories = [
    'Xerox',
    'Printing',
    'Binding',
    'Book Making',
    'Flex Banner',
    'Brand Board',
    'Graphic Designing',
    'Foam Sheet Printing',
    'MDF Sheet Printing',
    'Cardboard Printing',
    'Lamination',
    'Other',
  ];

  newOrder: any = {
    customer_id: '',
    order_category: '',
    description: '',
    amount: null,
  };
  editingOrder: any = null;

  customerMap: { [id: number]: string } = {};

  constructor(
    private orderService: OrderService,
    private customerService: CustomerService,
  ) {}

  ngOnInit(): void {
    this.customerService.getCustomers().subscribe((data) => {
      this.customers = data;
      this.filteredCustomers = data;
      this.customers.forEach((c) => (this.customerMap[c.id!] = c.name));
      this.loadOrders();
    });
  }

  filterCustomers() {
    const query = this.customerSearch.toLowerCase();
    this.filteredCustomers = this.customers.filter(
      (c) =>
        c.name.toLowerCase().includes(query) ||
        (c.phone && c.phone.includes(query)),
    );
  }

  loadOrders() {
    const cid = this.filterCustomerId ? +this.filterCustomerId : undefined;
    this.orderService.getOrders(cid).subscribe((data) => (this.orders = data));
  }

  getCustomerName(id: number): string {
    return this.customerMap[id] || `Unknown (${id})`;
  }

  selectCategory(cat: string) {
    this.newOrder.order_category = cat;
  }

  onSubmit() {
    this.orderService.createOrder(this.newOrder).subscribe((order) => {
      this.showCreateForm = false;
      this.newOrder = {
        customer_id: '',
        order_category: '',
        description: '',
        amount: null,
      };
      this.loadOrders();

      // WhatsApp Notification
      const c = this.customers.find((x) => x.id === order.customer_id);
      if (c && order.points_earned! > 0) {
        const msg = `Congratulations you have earned ${order.points_earned} points in your Sundaram Digital account. You can redeem these points on your next order.`;
        window.open(
          `https://wa.me/91${c.phone}/?text=${encodeURIComponent(msg)}`,
          '_blank',
        );
      }
    });
  }

  editOrder(order: Order) {
    this.editingOrder = { ...order };
  }

  cancelEdit() {
    this.editingOrder = null;
  }

  updateOrder() {
    if (this.editingOrder && this.editingOrder.id) {
      this.orderService
        .updateOrder(this.editingOrder.id, this.editingOrder)
        .subscribe(() => {
          this.editingOrder = null;
          this.loadOrders();
        });
    }
  }

  deleteOrder(id: number) {
    if (confirm('Are you sure you want to delete this order?')) {
      if (id !== undefined) {
        this.orderService.deleteOrder(id).subscribe(() => {
          this.loadOrders();
        });
      }
    }
  }
}
