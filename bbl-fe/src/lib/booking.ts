import { apiFetch } from "./api";

export interface CreateBookingRequest {
  topic: string;
  from_time: string;
  to_time: string;
  participants: string[];
}

export interface Booking {
  _id: string;
  topic: string;
  from_time: string;
  to_time: string;
  participants: string[];
}

export async function createBooking(data: CreateBookingRequest) {
  return apiFetch<{ message: string }>("/bookings", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getBookings() {
  return apiFetch<{
    message: string;
    data: Booking[];
  }>("/bookings");
}

export async function deleteBooking(id: string) {
  return apiFetch<{ message: string }>(`/bookings/${id}`, {
    method: "DELETE",
  });
}
