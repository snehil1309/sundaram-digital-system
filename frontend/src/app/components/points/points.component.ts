import { Component, OnInit } from '@angular/core';
import { CustomerService, Customer } from '../../services/customer.service';
import { PointsService, PointsHistory } from '../../services/points.service';

@Component({
  selector: 'app-points',
  templateUrl: './points.component.html'
})
export class PointsComponent implements OnInit {
  customers: Customer[] = [];
  redeemData: any = { customer_id: '', points_to_redeem: null };
  historyCustomerId: number | string = '';
  history: PointsHistory[] = [];
  error = '';
  message = '';

  constructor(private customerService: CustomerService, private pointsService: PointsService) { }

  ngOnInit() {
    this.loadCustomers();
  }

  loadCustomers() {
    this.customerService.getCustomers().subscribe(data => this.customers = data);
  }

  onRedeem() {
    this.error = '';
    this.message = '';

    const customer = this.customers.find(c => c.id === +this.redeemData.customer_id);
    if (customer && customer.total_points! < this.redeemData.points_to_redeem) {
      this.error = 'Insufficient points balance';
      return;
    }

    this.pointsService.redeemPoints(+this.redeemData.customer_id, this.redeemData.points_to_redeem).subscribe(
      (res) => {
        this.message = `Successfully redeemed. New Balance: ${res.remaining_balance}`;
        if (customer) {
          const msg = `You have successfully redeemed ${this.redeemData.points_to_redeem} points. Remaining balance in your Sundaram Digital account is ${res.remaining_balance}.`;
          window.open(`https://api.whatsapp.com/send?phone=91${customer.phone}&text=${encodeURIComponent(msg)}`, '_blank');
        }
        this.redeemData = { customer_id: '', points_to_redeem: null };
        this.loadCustomers(); // refresh points
      },
      (err) => {
        this.error = err.error?.detail || 'An error occurred';
      }
    );
  }

  loadHistory() {
    if (this.historyCustomerId) {
      this.pointsService.getPointsHistory(+this.historyCustomerId).subscribe(data => {
        this.history = data;
      });
    }
  }
}
