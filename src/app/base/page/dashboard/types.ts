export interface Group {
  id: number;
  name: string;
  simplify_by_default: boolean;
  members: Member[];
  cover_photo: CoverPhoto;
}

export interface Member {
  id: number;
  first_name: string;
  last_name: any;
  picture: Picture;
  custom_picture: boolean;
  email: string;
  registration_status: string;
  balance: Balance[];
}

export interface Picture {
  small: string;
  medium: string;
  large: string;
}

export interface Balance {
  amount: number;
  currency_code: string;
}

export interface CoverPhoto {
  xxlarge: string;
  xlarge: string;
}

export interface Friends {
  id: number;
  first_name: string;
  last_name: string;
  balance: Balance[];
  picture: Picture;
  updated_at: string;
}

export interface Picture {
  small: string;
  medium: string;
  large: string;
}
