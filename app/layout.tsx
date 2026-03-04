import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

export const metadata: Metadata = {
  title: "SMART AI NEXUS – Global AI Marketplace for Manufacturers & Buyers",
  description:
    "Find. Build. Buy. Instantly. SMART AI NEXUS is a global AI marketplace connecting manufacturers, businesses, builders and individual buyers.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
