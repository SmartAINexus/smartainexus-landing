import { NextResponse } from "next/server";

export function GET() {
  return NextResponse.json({
    service: "grantbridge-europe",
    status: "ok",
    dataMode: "synthetic-only",
  });
}
