export interface Profile {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  registration_status: string;
  picture: Picture;
  balance: Balance[];
  groups: Group[];
  updated_at: string;
  user_split: number;
  user_selected: boolean;
}

export interface Picture {
  small: string;
  medium: string;
  large: string;
}

export interface Balance {
  currency_code: string;
  amount: string;
}

export interface Group {
  group_id: number;
  balance: Balance[];
}
