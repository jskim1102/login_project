// src/services/userService.ts

import { prisma } from "@/lib/prisma";
import { hashPassword, verifyPassword } from "@/lib/security";
import { UserCreate } from "@/types/user";

export async function getUserByEmail(email: string) {
  return await prisma.user.findUnique({ where: { email } });
}

export async function createUser(user: UserCreate) {
  const hashedPassword = await hashPassword(user.password);
  return await prisma.user.create({
    data: {
      email: user.email,
      hashedPassword,
    },
  });
}

export async function authenticateUser(email: string, password: string) {
  const user = await getUserByEmail(email);
  if (!user) return null;

  const isValid = await verifyPassword(password, user.hashedPassword);
  if (!isValid) return null;

  return user;
}