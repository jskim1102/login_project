// src/app/api/token/route.ts

import { NextRequest, NextResponse } from "next/server";
import { authenticateUser } from "@/services/userService";
import { signJwt } from "@/lib/security";

export async function OPTIONS() {
  return new NextResponse(null, { status: 200 });
}

export async function POST(req: NextRequest) {
  const body = await req.json();
  const { email, password } = body;

  if (!email || !password) {
    return NextResponse.json(
      { message: "Email and password are required" },
      { status: 400 }
    );
  }

  const user = await authenticateUser(email, password);
  if (!user) {
    return NextResponse.json(
      { message: "Invalid email or password" },
      { status: 401 }
    );
  }

  const token = signJwt({ sub: user.email});
  
  return NextResponse.json(
    { access_token: token, token_type: "bearer" },
    { status: 200 }
  );
}