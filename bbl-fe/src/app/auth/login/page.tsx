"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/lib/auth";
import Link from "next/link";

export default function LoginPage() {
  const router = useRouter();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      setLoading(true);
      setError("");

      const res = await login({
        username,
        password,
      });

      localStorage.setItem("access_token", res.access_token);

      router.push("/booking");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6 w-full">
      <h1 className="text-2xl font-bold">Login</h1>

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

      {error && <p className="text-red-500">{error}</p>}

      <button
        onClick={handleLogin}
        disabled={loading}
        className="w-full border p-2"
      >
        {loading ? "Loading..." : "Login"}
      </button>
      <Link href="/auth/register">register here</Link>
    </div>
  );
}
