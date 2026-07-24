interface ProgressBarProps {
  percent: number;
  colorClassName?: string;
}

export function ProgressBar({ percent, colorClassName = "bg-terracotta-700" }: ProgressBarProps) {
  return (
    <div className="h-2 w-full rounded-full bg-ink/10 overflow-hidden">
      <div
        className={`h-full rounded-full transition-all duration-500 ${colorClassName}`}
        style={{ width: `${Math.min(100, Math.max(0, percent))}%` }}
      />
    </div>
  );
}
