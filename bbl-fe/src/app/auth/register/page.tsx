"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { register } from "@/lib/auth";
import Link from "next/link";

export default function RegisterPage() {
  const router = useRouter();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRegister = async () => {
    try {
      setLoading(true);
      setError("");

      if (password !== confirmPassword) {
        throw new Error("Passwords do not match");
      }

      await register({
        username,
        password,
      });

      router.push("/auth/login");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6 w-full">
      <h1 className="text-2xl font-bold">Register</h1>

      <input
        className="w-full border p-2"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        className="w-full border p-2"
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <input
        className="w-full border p-2"
        type="password"
        placeholder="Confirm Password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
      />

      {error && <p className="text-red-500">{error}</p>}

      <button
        onClick={handleRegister}
        disabled={loading}
        className="w-full border p-2"
      >
        {loading ? "Loading..." : "Register"}
      </button>
      <Link href="/auth/login">login here</Link>
    </div>
  );
}
