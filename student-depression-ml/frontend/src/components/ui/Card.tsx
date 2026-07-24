import type { HTMLAttributes, ReactNode } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  variant?: "solid" | "glass";
}

export function Card({ className = "", children, variant = "solid", ...rest }: CardProps) {
  const base =
    variant === "glass"
      ? "glass rounded-3xl"
      : "rounded-3xl bg-surface shadow-[0_20px_50px_-25px_rgba(43,42,38,0.25)] dark:shadow-[0_20px_50px_-25px_rgba(0,0,0,0.6)]";

  return (
    <div className={`${base} ${className}`} {...rest}>
      {children}
    </div>
  );
}
