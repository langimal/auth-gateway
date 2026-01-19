// types.ts
export interface User {
  id: string;
  username: string;
  email: string;
  password: string;
  role: Role;
}

export enum Role {
  ADMIN = 'admin',
  USER = 'user',
}

export interface AuthenticationRequest {
  username: string;
  password: string;
}

export interface AuthenticationResponse {
  token: string;
  user: User;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface ErrorResponse {
  code: number;
  message: string;
}