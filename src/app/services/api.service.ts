import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  API_BASE = environment.host;
  constructor(private httpClient: HttpClient) {}

  oAuth() {}
  getUser() {}
  getGroups() {
    return this.httpClient.get(`${this.API_BASE}/groups`);
  }
  getFriends() {
    return this.httpClient.get(`${this.API_BASE}/friends`);
  }
  getDetails(type: string, id: number, data: any) {
    return this.httpClient.get(`${this.API_BASE}/${type}/${id}`, {
      params: data,
    });
  }
  getProfile() {
    return this.httpClient.get(`${this.API_BASE}/profile`);
  }

  saveExpense(type: string, id: number, data: any) {
    return this.httpClient.post(`${this.API_BASE}/${type}/${id}`, data);
  }
}
