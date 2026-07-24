interface SliderProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step?: number;
  unit?: string;
  minLabel?: string;
  maxLabel?: string;
  color?: "sage" | "terracotta";
  onChange: (value: number) => void;
}

const COLOR_HEX: Record<NonNullable<SliderProps["color"]>, string> = {
  sage: "#4c7a5a",
  terracotta: "#c97b5a",
};

const BADGE_CLASSES: Record<NonNullable<SliderProps["color"]>, string> = {
  sage: "bg-sage-50 text-sage-700",
  terracotta: "bg-peach-100 text-terracotta-700",
};

export function Slider({
  label,
  value,
  min,
  max,
  step = 1,
  unit = "",
  minLabel,
  maxLabel,
  color = "sage",
  onChange,
}: SliderProps) {
  const fillPercent = ((value - min) / (max - min)) * 100;

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <span className="text-lg text-ink">{label}</span>
        <span className={`rounded-full px-3 py-1 text-sm font-semibold font-heading ${BADGE_CLASSES[color]}`}>
          {value}
          {unit}
        </span>
      </div>
      <input
        type="range"
        className="app-slider"
        style={{ "--thumb-color": COLOR_HEX[color], "--fill": `${fillPercent}%` } as React.CSSProperties}
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      />
      <div className="flex justify-between mt-2 text-sm text-ink-soft">
        <span>{minLabel ?? `${min}${unit}`}</span>
        <span>{maxLabel ?? `${max}${unit}`}</span>
      </div>
    </div>
  );
}
