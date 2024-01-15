import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { ApiService } from '../services/api.service';
import { ProfileServie } from '../services/profile';
import { Profile } from './profile';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-add-expense',
  templateUrl: './add-expense.page.html',
  styleUrls: ['./add-expense.page.scss'],
})
export class AddExpensePage implements OnInit, OnDestroy {
  private routeSub: Subscription;
  TYPE: string = '';
  ID: number = -Infinity;
  users: Profile[] = [];
  maxDate = new Date().toISOString();
  isAlertOpen = false;
  alertMessage = '';
  alertHeader = '';
  expenseForm: FormGroup = new FormGroup({
    cost: new FormControl('', [Validators.required]),
    description: new FormControl('', [Validators.required]),
    date: new FormControl('', [Validators.required]),
    paid_by: new FormControl('', [Validators.required]),
  });
  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private profileService: ProfileServie
  ) {
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

    this.apiService.getDetails(this.TYPE, this.ID, { fetch_all: 0 }).subscribe({
      next: (e: any) => {
        if (this.TYPE === 'friend') {
          this.users.push(e['detail']);

          this.profileService.getProfile().subscribe((d: any) => {
            if (Object.keys(d).length === 0) {
              return;
            }
            this.users.push(d);
          });
        }

        if (this.TYPE === 'group') {
          this.users = e['detail']['members'];
        }
        this.users.map((e) => (e.user_selected = true));
      },
    });
    this.expenseForm.controls['cost'].valueChanges.subscribe({
      next: (_d) => this.changeAmount(),
    });
  }
  ngOnDestroy() {
    this.routeSub.unsubscribe();
  }
  selectDate(ev: any) {
    this.expenseForm.controls['date'].setValue(
      new Date(Date.parse(ev.detail.value)).toISOString().split('T')[0]
    );
    console.log(this.expenseForm.value);
  }
  changeAmount() {
    const amount = parseFloat(this.expenseForm.controls['cost'].value);
    if (!amount) {
      return;
    }
    const between = this.users.filter((e) => e.user_selected).length;
    const indSplit = amount / between;
    this.users.forEach((e) => {
      if (e.user_selected) {
        e.user_split = indSplit;
      } else {
        e.user_split = 0;
      }
    });
  }
  revampUsers(i: number, ev: any) {
    this.users[i].user_selected = ev.detail.checked;
    this.changeAmount();
  }
  saveForm() {
    const incl = this.users.filter((e) => e.user_selected).length;
    if (!incl) {
      this.alertMessage = 'Please Select atleast one user';
      this.isAlertOpen = true;
      this.alertHeader = 'Validation Failed';
    }

    const formValue = this.expenseForm.value;
    formValue['date'] = new Date(formValue['date']).toISOString();
    formValue['members'] = this.users
      .filter((e) => e.user_selected)
      .flatMap((e) => e.id);
    this.apiService.saveExpense(this.TYPE, this.ID, formValue).subscribe({
      next: (d) => {
        this.isAlertOpen = true;
        this.alertMessage = 'Expense Added!';
        this.alertHeader = 'Suceess';
        this.expenseForm.reset();
        this.users.forEach((e) => (e.user_split = 0));
      },
    });
  }
  setOpen(isOpen: boolean) {
    this.isAlertOpen = isOpen;
    this.alertMessage = '';
  }
}
