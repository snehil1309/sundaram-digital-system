import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
    providedIn: 'root'
})
export class AuthService {
    private apiUrl = 'http://localhost:8000/api';
    private loggedIn = new BehaviorSubject<boolean>(this.hasToken());

    constructor(private http: HttpClient) { }

    hasToken(): boolean {
        return !!localStorage.getItem('token');
    }

    isLoggedIn(): Observable<boolean> {
        return this.loggedIn.asObservable();
    }

    login(credentials: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/login`, credentials).pipe(
            tap((res: any) => {
                if (res.token) {
                    localStorage.setItem('token', res.token);
                    this.loggedIn.next(true);
                }
            })
        );
    }

    logout(): void {
        localStorage.removeItem('token');
        this.loggedIn.next(false);
    }
}
