"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/openai-server/feature/agentic_chat");
  }, [router]);
  return null;
}
