import { BehaviorSubject } from 'rxjs';

export class ProfileServie {
  private profile = new BehaviorSubject({});

  setProfile(profile: any) {
    this.profile.next(profile);
  }
  getProfile() {
    return this.profile.asObservable();
  }
}
