import { apiFetch } from "./api";

export interface AuthRequest {
  username: string;
  password: string;
}

export async function login(data: AuthRequest) {
  return apiFetch<{
    message: string;
    access_token: string;
  }>("/auth/login", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function register(data: AuthRequest) {
  return apiFetch<{
    message: string;
  }>("/auth/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
