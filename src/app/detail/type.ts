export interface Expense {
  cost: string;
  description: string;
  details: any;
  date: string;
  currency_code: string;
  friendship_id: any;
  created_by: CreatedBy;
  users: User[];
}

export interface CreatedBy {
  id: number;
  first_name: string;
  last_name: any;
  picture: Picture;
  custom_picture: boolean;
}

export interface Picture {
  medium: string;
}

export interface User {
  user: UserInfo;
  user_id: number;
  paid_share: string;
  owed_share: string;
  net_balance: number;
}

export interface UserInfo {
  id: number;
  first_name: string;
  last_name?: string;
  picture: Picture;
}

export interface detailInfo {
  id: number;
  first_name: string;
  last_name: any;
  email: string;
  registration_status: string;
  picture: Picture;
  balance: Balance[];
  groups: Group[];
  updated_at: string;
  name: string;
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
