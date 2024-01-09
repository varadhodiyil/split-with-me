import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';
import { Balance, Friends, Group, Member } from './types';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPage implements OnInit {
  constructor(private apiService: ApiService) {}
  groups: Group[] = [];
  friends: Friends[] = [];
  tabs = {
    FRIENDS: 1,
    GROUPS: 2,
  };
  currentTab = this.tabs.GROUPS;
  sort(arr: any[], key: string) {
    return arr.sort((a, b) => (a[key] as string).localeCompare(b[key]));
  }
  switchTab() {
    this.friends = [];
    this.groups = [];
    if (this.currentTab == this.tabs.FRIENDS) {
      this.apiService.getGroups().subscribe({
        next: (d: any) => (this.groups = d['result']),
      });
      this.currentTab = this.tabs.GROUPS;
    } else {
      this.apiService.getFriends().subscribe({
        next: (d: any) => (this.friends = d['result']),
      });
      this.currentTab = this.tabs.FRIENDS;
    }
  }
  ngOnInit() {
    this.switchTab();
  }
  getTotal(members: Member[] = []): { amount: number; curreny: string }[] {
    const mapped: any = {};
    members.forEach((member) => {
      member.balance.forEach((e) => {
        mapped[e.currency_code] =
          mapped[e.currency_code] || 0 + parseFloat(`${e.amount}`);
      });
    });
    return Object.entries(mapped).map((e: any) => {
      return { amount: e[1], curreny: e[0] };
    });
  }
  getCode(members: Member[]) {
    return members[0].balance[0].amount;
  }
}
