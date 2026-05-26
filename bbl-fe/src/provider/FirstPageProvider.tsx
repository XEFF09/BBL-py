"use client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function FirstPageProvider({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const router = useRouter();

  useEffect(() => {
    router.push("/auth/login");
  }, []);

  return <div>{children}</div>;
}
