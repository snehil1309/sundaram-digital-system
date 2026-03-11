import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ReportService {
    private apiUrl = 'https://sundaram-digital-system.onrender.com/api/reports';

    constructor(private http: HttpClient) { }

    getDashboardStats(): Observable<any> {
        return this.http.get(`${this.apiUrl}/dashboard`);
    }

    getSalesReport(period: string): Observable<any> {
        return this.http.get(`${this.apiUrl}/sales?period=${period}`);
    }

    getTopCustomers(): Observable<any> {
        return this.http.get(`${this.apiUrl}/top-customers`);
    }
}
