import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpErrorResponse,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private router: Router) {}

  intercept(req: HttpRequest<any>, next: HttpHandler) {
    // Get the auth token from the service.

    // Clone the request and replace the original headers with
    // cloned headers, updated with the authorization.

    const authReq = req.clone({
      headers: req.headers.set(
        'Authorization',
        `${localStorage.getItem('AuthToken')}`
      ),
    });
    authReq.headers.append('enableCors', 'false');

    // send cloned request with header to the next handler.
    return next.handle(authReq).pipe(
      catchError((error: any) => {
        if (error instanceof HttpErrorResponse && error.status === 401) {
          localStorage.clear();
          this.router.navigate(['/auth/login']);
          return throwError(() => error);
        } else {
          return throwError(() => error);
        }
      })
    );
  }
}
