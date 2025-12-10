// types.ts
export interface User {
  id: string;
  username: string;
  email: string;
  password: string;
  roles: string[];
}

export interface AccessToken {
  token: string;
  expiresAt: number;
}

export interface RefreshToken {
  token: string;
  expiresAt: number;
}

export interface AuthResponse {
  accessToken: AccessToken;
  refreshToken: RefreshToken;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface ErrorResponse {
  message: string;
  statusCode: number;
}