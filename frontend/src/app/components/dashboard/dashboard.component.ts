import { Component, OnInit } from '@angular/core';
import { ReportService } from '../../services/report.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
})
export class DashboardComponent implements OnInit {
  stats: any = {};

  constructor(private reportService: ReportService) {}

  ngOnInit(): void {
    this.reportService.getDashboardStats().subscribe((data) => {
      this.stats = data;
    });
  }
}
