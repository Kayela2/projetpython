import { useOnboarding } from "../../context/OnboardingContext";
import { useLanguage } from "../../context/LanguageContext";

function moodEmoji(stress: number): string {
  if (stress <= 2) return "😌";
  if (stress <= 4) return "🙂";
  if (stress <= 6) return "😐";
  if (stress <= 8) return "😟";
  return "😩";
}

export function StepFeelings() {
  const { data, updateData } = useOnboarding();
  const { t } = useLanguage();

  return (
    <div className="text-center">
      <h2 className="text-3xl font-semibold text-sage-700 dark:text-sage-300">{t.stepFeelings.title}</h2>
      <p className="mx-auto mt-3 max-w-md text-ink-soft">{t.stepFeelings.subtitle}</p>

      <div className="mt-10 flex items-center justify-center gap-10">
        <div className="text-center text-sm text-ink-soft">
          <span className="text-2xl">🌿</span>
          <p className="mt-1">{t.stepFeelings.calm}</p>
        </div>

        <div className="text-center">
          <div className="text-6xl">{moodEmoji(data.stressLevel)}</div>
          <p className="mt-2 font-heading text-2xl font-semibold text-ink">{data.stressLevel} / 10</p>
        </div>

        <div className="text-center text-sm text-ink-soft">
          <span className="text-2xl">🥵</span>
          <p className="mt-1">{t.stepFeelings.exhausted}</p>
        </div>
      </div>

      <div className="mx-auto mt-8 max-w-md">
        <input
          type="range"
          className="app-slider"
          style={{ "--thumb-color": "#4c7a5a", "--fill": `${((data.stressLevel - 1) / 9) * 100}%` } as React.CSSProperties}
          min={1}
          max={10}
          step={1}
          value={data.stressLevel}
          onChange={(e) => updateData({ stressLevel: Number(e.target.value) })}
        />
        <div className="mt-2 flex justify-between text-xs text-ink-soft">
          {Array.from({ length: 10 }, (_, i) => (
            <span key={i}>{i + 1}</span>
          ))}
        </div>
      </div>

      <p className="mt-10 text-sm italic text-ink-soft">{t.stepFeelings.quote}</p>
    </div>
  );
}
