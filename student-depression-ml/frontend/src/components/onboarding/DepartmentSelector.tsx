import type { Department } from "../../types/prediction";
import { useLanguage } from "../../context/LanguageContext";

const DEPARTMENTS: { value: Department; emoji: string }[] = [
  { value: "Science", emoji: "🧪" },
  { value: "Engineering", emoji: "⚙️" },
  { value: "Arts", emoji: "🎨" },
  { value: "Medical", emoji: "🩺" },
  { value: "Business", emoji: "💼" },
];

interface DepartmentSelectorProps {
  value: Department | null;
  onChange: (value: Department) => void;
}

export function DepartmentSelector({ value, onChange }: DepartmentSelectorProps) {
  const { t } = useLanguage();

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-5">
      {DEPARTMENTS.map((dept) => {
        const selected = dept.value === value;
        return (
          <button
            key={dept.value}
            type="button"
            onClick={() => onChange(dept.value)}
            className={`lift-hover-sm flex flex-col items-center gap-2 rounded-2xl border p-4 ${
              selected ? "border-sage-700 bg-sage-50" : "border-transparent bg-cream-dark hover:border-sage-200"
            }`}
          >
            <span className="flex h-11 w-11 items-center justify-center rounded-full bg-surface text-xl">
              {dept.emoji}
            </span>
            <span className="text-sm font-medium text-ink">{t.departments[dept.value]}</span>
          </button>
        );
      })}
    </div>
  );
}
