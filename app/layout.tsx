import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "GrantBridge Europe",
  description: "A megfelelő támogatástól a kész pályázatig.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="hu">
      <body>{children}</body>
    </html>
  );
}
