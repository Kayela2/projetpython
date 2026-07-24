import { useOnboarding } from "../../context/OnboardingContext";
import { useLanguage } from "../../context/LanguageContext";
import { Slider } from "../ui/Slider";

export function StepAcademics() {
  const { data, updateData } = useOnboarding();
  const { t } = useLanguage();

  return (
    <div>
      <h2 className="text-3xl font-semibold text-ink text-center">{t.stepAcademics.title}</h2>
      <p className="mt-3 text-center text-ink-soft">{t.stepAcademics.subtitle}</p>

      <div className="mt-10 space-y-10">
        <Slider
          label={t.stepAcademics.cgpaLabel}
          value={data.cgpa}
          min={0}
          max={4}
          step={0.1}
          color="sage"
          minLabel="0.0"
          maxLabel="4.0"
          onChange={(cgpa) => updateData({ cgpa })}
        />

        <Slider
          label={t.stepAcademics.studyHoursLabel}
          value={data.studyHours}
          min={0}
          max={12}
          step={0.5}
          unit="h"
          color="terracotta"
          minLabel={t.stepAcademics.studyHoursMin}
          maxLabel={t.stepAcademics.studyHoursMax}
          onChange={(studyHours) => updateData({ studyHours })}
        />
      </div>
    </div>
  );
}
