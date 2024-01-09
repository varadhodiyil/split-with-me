import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { ApiService } from '../services/api.service';
import { Expense, detailInfo } from './type';
import { InfiniteScrollCustomEvent } from '@ionic/angular';

@Component({
  selector: 'app-detail',
  templateUrl: './detail.page.html',
  styleUrls: ['./detail.page.scss'],
})
export class DetailPage implements OnInit, OnDestroy {
  private routeSub: Subscription;
  TYPE: string = '';
  ID: number = -Infinity;
  limit: number = 20;
  details: Expense[] = [];
  currentPage = 0;
  detailInfo: detailInfo | null = null;

  constructor(private route: ActivatedRoute, private apiService: ApiService) {
    this.routeSub = this.route.params.subscribe(
      (params: { [x: string]: any }) => {
        this.TYPE = params['type'];
        this.ID = params['id'];
      }
    );
  }

  ngOnInit() {
    if (!this.ID) {
      return;
    }
    this.fetchPage(0);
  }
  fetchPage(page: number) {
    return this.apiService
      .getDetails(this.TYPE, this.ID, {
        limit: this.limit,
        page: page,
      })
      .subscribe({
        next: (d: any) => {
          if (d['detail']) {
            this.detailInfo = d['detail'];
          }
          this.details = this.details.concat(...d['result']);

          this.currentPage = page;
        },
      });
  }
  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }
  onIonInfinite(ev: any) {
    this.fetchPage(this.currentPage + 1);
    setTimeout(() => {
      (ev as InfiniteScrollCustomEvent).target.complete();
    }, 500);
  }
}
