import type { ButtonHTMLAttributes, ReactNode } from "react";

type Variant = "primary" | "accent" | "outline" | "ghost";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  children: ReactNode;
}

const VARIANT_CLASSES: Record<Variant, string> = {
  primary:
    "bg-sage-700 text-white shadow-sm shadow-sage-700/20 hover:bg-sage-900 hover:shadow-xl hover:shadow-sage-700/40 hover:-translate-y-0.5 active:translate-y-0",
  accent:
    "bg-terracotta-700 text-white shadow-sm shadow-terracotta-700/20 hover:bg-terracotta-800 hover:shadow-xl hover:shadow-terracotta-700/40 hover:-translate-y-0.5 active:translate-y-0",
  outline:
    "bg-surface text-ink border border-ink/10 hover:border-ink/25 hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0",
  ghost:
    "bg-transparent text-ink-soft hover:text-ink",
};

export function Button({ variant = "primary", className = "", children, ...rest }: ButtonProps) {
  return (
    <button
      className={`inline-flex items-center justify-center gap-1.5 rounded-full px-4 py-2.5 text-sm font-heading font-semibold transition-all duration-200 ease-out disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:translate-y-0 disabled:hover:shadow-none sm:gap-2 sm:px-7 sm:py-3.5 sm:text-base ${VARIANT_CLASSES[variant]} ${className}`}
      {...rest}
    >
      {children}
    </button>
  );
}
