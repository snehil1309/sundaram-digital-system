import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class BackupService {
    private apiUrl = 'https://sundaram-digital-system.onrender.com/api';

    constructor(private http: HttpClient) { }

    backupDatabase(): Observable<any> {
        return this.http.post(`${this.apiUrl}/backup`, {});
    }
}
