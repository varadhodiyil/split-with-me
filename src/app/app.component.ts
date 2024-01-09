import { Component, OnInit } from '@angular/core';
import { ApiService } from './services/api.service';
import { ProfileServie } from './services/profile';
@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
})
export class AppComponent implements OnInit {
  constructor(
    private apiService: ApiService,
    private profileService: ProfileServie
  ) {}
  ngOnInit(): void {
    this.apiService.getProfile().subscribe({
      next: (e: any) => this.profileService.setProfile(e['result']),
    });
  }
}
