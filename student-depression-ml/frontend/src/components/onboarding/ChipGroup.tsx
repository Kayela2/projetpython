interface ChipOption<T extends string> {
  value: T;
  label: string;
}

interface ChipGroupProps<T extends string> {
  options: ChipOption<T>[];
  value: T | null;
  onChange: (value: T) => void;
}

export function ChipGroup<T extends string>({ options, value, onChange }: ChipGroupProps<T>) {
  return (
    <div className="flex flex-wrap gap-3">
      {options.map((option) => {
        const selected = option.value === value;
        return (
          <button
            key={option.value}
            type="button"
            onClick={() => onChange(option.value)}
            className={`lift-hover-sm rounded-full border px-5 py-2.5 font-heading font-semibold ${
              selected
                ? "border-sage-700 bg-sage-700 text-white"
                : "border-ink/15 bg-surface text-ink hover:border-sage-400"
            }`}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}
