interface SpinnerProps {
  size?: number;
  className?: string;
}

export function Spinner({ size = 64, className = "" }: SpinnerProps) {
  return (
    <div
      role="status"
      aria-label="Chargement en cours"
      className={`inline-block animate-spin rounded-full border-[5px] border-sage-100 border-t-terracotta-700 ${className}`}
      style={{ width: size, height: size }}
    />
  );
}
