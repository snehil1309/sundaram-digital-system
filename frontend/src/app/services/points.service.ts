import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface PointsHistory {
    id: number;
    customer_id: number;
    order_id?: number;
    points_added: number;
    points_redeemed: number;
    balance_points: number;
    date: string;
}

@Injectable({
    providedIn: 'root'
})
export class PointsService {
    private apiUrl = 'http://localhost:8000/api';

    constructor(private http: HttpClient) { }

    redeemPoints(customerId: number, pointsToRedeem: number): Observable<any> {
        return this.http.post(`${this.apiUrl}/redeem-points`, {
            customer_id: customerId,
            points_to_redeem: pointsToRedeem
        });
    }

    getPointsHistory(customerId: number): Observable<PointsHistory[]> {
        return this.http.get<PointsHistory[]>(`${this.apiUrl}/points-history/${customerId}`);
    }
}
