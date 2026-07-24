import { useOnboarding } from "../../context/OnboardingContext";
import { useLanguage } from "../../context/LanguageContext";
import { Slider } from "../ui/Slider";
import deskImage from "../../assets/desk-scene.png";

export function StepLifestyle() {
  const { data, updateData } = useOnboarding();
  const { t } = useLanguage();

  return (
    <div className="grid grid-cols-1 items-center gap-10 md:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)]">
      <div className="hidden md:block">
        <img
          src={deskImage}
          alt={t.stepLifestyle.imageAlt}
          className="w-full rounded-3xl object-cover shadow-lg dark:ring-1 dark:ring-white/10"
        />
        <p className="mt-4 font-heading text-lg font-semibold text-terracotta-700 dark:text-terracotta-300">
          {t.stepLifestyle.imageCaption}
        </p>
        <p className="mt-1 text-sm text-ink-soft">{t.stepLifestyle.imageText}</p>
      </div>

      <div>
        <h2 className="text-3xl font-semibold text-ink">{t.stepLifestyle.title}</h2>

        <div className="mt-8 space-y-10">
          <Slider
            label={t.stepLifestyle.sleepLabel}
            value={data.sleepDuration}
            min={0}
            max={12}
            step={0.5}
            unit="h"
            color="sage"
            minLabel={t.stepLifestyle.sleepMin}
            maxLabel={t.stepLifestyle.sleepMax}
            onChange={(sleepDuration) => updateData({ sleepDuration })}
          />
          <Slider
            label={t.stepLifestyle.socialLabel}
            value={data.socialMediaHours}
            min={0}
            max={10}
            step={0.5}
            unit={t.stepLifestyle.socialUnit}
            color="terracotta"
            minLabel={t.stepLifestyle.socialMin}
            maxLabel={t.stepLifestyle.socialMax}
            onChange={(socialMediaHours) => updateData({ socialMediaHours })}
          />
          <Slider
            label={t.stepLifestyle.activityLabel}
            value={data.physicalActivity}
            min={0}
            max={150}
            step={5}
            unit={t.stepLifestyle.activityUnit}
            color="sage"
            minLabel={t.stepLifestyle.activityMin}
            maxLabel={t.stepLifestyle.activityMax}
            onChange={(physicalActivity) => updateData({ physicalActivity })}
          />
        </div>
      </div>
    </div>
  );
}
