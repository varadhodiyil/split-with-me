import { Component, OnInit } from '@angular/core';
import { ActivationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-base',
  templateUrl: './base.page.html',
  styleUrls: ['./base.page.scss'],
})
export class BasePage implements OnInit {
  title = '';
  constructor(private router: Router) {}

  ngOnInit() {
    this.router.events.subscribe((data) => {
      if (data instanceof ActivationEnd) {
        if (data.snapshot.data['title'])
          this.title = data.snapshot.data['title'];
      }
    });
  }
}
