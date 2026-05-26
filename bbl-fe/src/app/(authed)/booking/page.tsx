"use client";

import { useEffect, useState } from "react";
import {
  Booking,
  getBookings,
  deleteBooking,
  createBooking,
} from "@/lib/booking";

export default function BookingPage() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);

  const [topic, setTopic] = useState("");
  const [fromTime, setFromTime] = useState("");
  const [toTime, setToTime] = useState("");
  const [participants, setParticipants] = useState("");

  const loadBookings = async () => {
    try {
      const res = await getBookings();
      setBookings(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBookings();
  }, []);

  const handleCreateBooking = async () => {
    try {
      await createBooking({
        topic,
        from_time: fromTime,
        to_time: toTime,
        participants: participants.split(",").map((p) => p.trim()),
      });

      await loadBookings();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteBooking(id);

      await loadBookings();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-4 rounded border p-4">
        <h1 className="text-xl font-bold">Create Booking</h1>

        <input
          type="text"
          placeholder="Topic"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          className="border p-2"
        />

        <input
          type="text"
          placeholder="From Time (10:00AM)"
          value={fromTime}
          onChange={(e) => setFromTime(e.target.value)}
          className="border p-2"
        />

        <input
          type="text"
          placeholder="To Time (10:30AM)"
          value={toTime}
          onChange={(e) => setToTime(e.target.value)}
          className="border p-2"
        />

        <input
          type="text"
          placeholder="Participants comma separated"
          value={participants}
          onChange={(e) => setParticipants(e.target.value)}
          className="border p-2"
        />

        <button onClick={handleCreateBooking} className="border p-2">
          Create Booking
        </button>
      </div>
      {bookings.map((booking) => (
        <div key={booking._id} className="rounded border p-4">
          <h2 className="font-bold">{booking.topic}</h2>

          <p>
            {booking.from_time} - {booking.to_time}
          </p>

          <p>Participants: {booking.participants.join(", ")}</p>

          <button
            onClick={() => handleDelete(booking._id)}
            className="mt-2 border px-3 py-1"
          >
            Delete
          </button>
        </div>
      ))}
    </div>
  );
}
