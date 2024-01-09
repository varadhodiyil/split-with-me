import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { BasePage } from './base.page';

const routes: Routes = [
  {
    path: '',
    component: BasePage,
    children: [
      {
        path: 'dashboard',
        data: {
          title: 'Dashboard',
        },
        loadChildren: () =>
          import('./page/dashboard/dashboard.module').then(
            (d) => d.DashboardPageModule
          ),
      },
      {
        path: '**',
        redirectTo: 'dashboard',
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class BasePageRoutingModule {}
