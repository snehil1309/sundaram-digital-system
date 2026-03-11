import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Order {
    id?: number;
    invoice_number?: string;
    customer_id: number;
    order_category: string;
    description?: string;
    amount: number;
    points_earned?: number;
    created_at?: string;
}

@Injectable({
    providedIn: 'root'
})
export class OrderService {
    private apiUrl = 'https://sundaram-digital-system.onrender.com/api';

    constructor(private http: HttpClient) { }

    getOrders(customerId?: number): Observable<Order[]> {
        const url = customerId ? `${this.apiUrl}/orders?customer_id=${customerId}` : `${this.apiUrl}/orders`;
        return this.http.get<Order[]>(url);
    }

    createOrder(order: Order): Observable<Order> {
        return this.http.post<Order>(`${this.apiUrl}/order`, order);
    }

    updateOrder(id: number, order: Order): Observable<Order> {
        return this.http.put<Order>(`${this.apiUrl}/order/${id}`, order);
    }

    deleteOrder(id: number): Observable<any> {
        return this.http.delete(`${this.apiUrl}/order/${id}`);
    }
}
