import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'auth',
    loadChildren: () => import('./auth/auth.module').then((a) => a.AuthModule),
  },
  {
    path: 'base',
    loadChildren: () =>
      import('./base/base.module').then((m) => m.BasePageModule),
  },
  {
    path: 'detail',
    loadChildren: () =>
      import('./detail/detail.module').then((m) => m.DetailPageModule),
  },

  {
    path: 'add-expense',
    loadChildren: () =>
      import('./add-expense/add-expense.module').then(
        (m) => m.AddExpensePageModule
      ),
  },
  {
    path: '**',
    redirectTo: 'base',
  },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules }),
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}
