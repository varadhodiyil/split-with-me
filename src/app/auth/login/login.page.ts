import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage {
  loginForm = new FormGroup({
    api_key: new FormControl('', [Validators.required]),
  });
  constructor(private router: Router) {}

  login() {
    const token = this.loginForm.controls['api_key'].value;
    if (!token) {
      return;
    }
    localStorage.setItem('AuthToken', token);
    this.router.navigate(['/base']);
  }
}
