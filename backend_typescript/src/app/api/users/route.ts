// src/app/api/users/route.ts

import { NextRequest, NextResponse } from "next/server";
import { createUser, getUserByEmail } from "@/services/userService";
import { UserCreate } from "@/types/user";

export async function OPTIONS() {
  return new NextResponse(null, { status: 200 });
}

export async function POST(req: NextRequest) {
  const body = await req.json();
  const { email, password} = body as UserCreate;

  if (!email || !password) {
    return NextResponse.json(
      { message: "모든 필드를 입력해 주세요." },
      { status: 400 }
    );
  }

  const existing = await getUserByEmail(email);
  if (existing) {
    return NextResponse.json(
      { message: "이미 등록된 이메일입니다." },
      { status: 400 }
    );
  }

  const user = await createUser({ email, password});
  const { hashedPassword, ...userWithoutPassword } = user;
  return NextResponse.json(userWithoutPassword, { status: 201 });
}