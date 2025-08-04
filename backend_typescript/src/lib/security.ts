// src/lib/security.ts

import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

export async function hashPassword(password: string) {
  return await bcrypt.hash(password, 10);
}

export async function verifyPassword(password: string, hash: string) {
  return await bcrypt.compare(password, hash);
}

export function signJwt(payload: object) {
  return jwt.sign(payload, process.env.JWT_SECRET as string, {
    expiresIn: process.env.JWT_EXPIRES_IN || "60m",
  });
}