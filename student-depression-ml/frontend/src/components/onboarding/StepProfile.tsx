import { useOnboarding } from "../../context/OnboardingContext";
import { useLanguage } from "../../context/LanguageContext";
import { Slider } from "../ui/Slider";
import { ChipGroup } from "./ChipGroup";
import { DepartmentSelector } from "./DepartmentSelector";
import type { Gender } from "../../types/prediction";

export function StepProfile() {
  const { data, updateData } = useOnboarding();
  const { t } = useLanguage();

  const genderOptions: { value: Gender; label: string }[] = [
    { value: "Female", label: t.gender.female },
    { value: "Male", label: t.gender.male },
  ];

  return (
    <div>
      <h2 className="text-3xl font-semibold text-ink text-center">{t.stepProfile.title}</h2>
      <p className="mt-3 text-center text-ink-soft">{t.stepProfile.subtitle}</p>

      <div className="mt-10 space-y-10">
        <Slider
          label={t.stepProfile.ageQuestion}
          value={data.age}
          min={18}
          max={24}
          unit={t.stepProfile.ageUnit}
          minLabel={t.stepProfile.ageMinLabel}
          maxLabel={t.stepProfile.ageMaxLabel}
          onChange={(age) => updateData({ age })}
        />

        <div>
          <p className="mb-3 text-lg text-ink">{t.stepProfile.genderQuestion}</p>
          <ChipGroup options={genderOptions} value={data.gender} onChange={(gender) => updateData({ gender })} />
        </div>

        <div>
          <p className="mb-3 text-lg text-ink">{t.stepProfile.departmentQuestion}</p>
          <DepartmentSelector value={data.department} onChange={(department) => updateData({ department })} />
        </div>
      </div>
    </div>
  );
}
