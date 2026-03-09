import { Component, OnInit } from '@angular/core';
import { ReportService } from '../../services/report.service';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html'
})
export class ReportsComponent implements OnInit {
  salesData: any = null;
  topCustomers: any[] = [];

  constructor(private reportService: ReportService) { }

  ngOnInit() {
    this.loadSales('daily');
    this.reportService.getTopCustomers().subscribe(data => this.topCustomers = data);
  }

  loadSales(period: string) {
    this.reportService.getSalesReport(period).subscribe(data => this.salesData = data);
  }
}
