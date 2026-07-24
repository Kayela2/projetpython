import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Button } from "../components/ui/Button";
import { BrainIcon, CheckIcon, CompassIcon, HeartIcon, MoonIcon, PhoneIcon } from "../components/icons";
import type { FeatureContribution, PredictionResponse } from "../types/prediction";
import { useOnboarding } from "../context/OnboardingContext";
import { useLanguage } from "../context/LanguageContext";
import type { Translations } from "../i18n/translations";

function factorIcon(feature: string) {
  if (feature === "Sleep_Duration") return MoonIcon;
  if (feature === "Stress_Level") return BrainIcon;
  if (feature === "Physical_Activity") return HeartIcon;
  return CompassIcon;
}

function FactorCard({
  factor,
  maxAbs,
  t,
}: {
  factor: FeatureContribution;
  maxAbs: number;
  t: Translations;
}) {
  const Icon = factorIcon(factor.feature);
  const pct = maxAbs > 0 ? Math.round((Math.abs(factor.contribution) / maxAbs) * 100) : 0;
  const barColor = factor.direction === "increases_risk" ? "bg-terracotta-500" : "bg-sage-600";
  // Labels are translated locally from the feature key rather than using the
  // backend's `label` (always French) — keeps prediction text language-agnostic
  // without needing to pass a locale to the API.
  const label = t.featureLabels[factor.feature] ?? factor.feature;
  const impactText =
    factor.direction === "increases_risk"
      ? t.results.increasesRisk
      : factor.direction === "decreases_risk"
        ? t.results.decreasesRisk
        : t.results.neutralImpact;

  return (
    <div className="glass lift-hover-sm rounded-3xl p-6">
      <span className="flex h-11 w-11 items-center justify-center rounded-full bg-cream-dark">
        <Icon className="h-5 w-5 text-ink" />
      </span>
      <h3 className="mt-4 text-lg font-semibold text-ink">{label}</h3>
      <p className="mt-1 text-sm text-ink-soft">
        {t.results.factorValueLabel} : <span className="font-medium text-ink">{factor.value}</span> — {impactText}
      </p>
      <div className="mt-4 flex items-center gap-3">
        <div className="h-2 flex-1 rounded-full bg-ink/10 overflow-hidden">
          <div className={`h-full rounded-full ${barColor}`} style={{ width: `${pct}%` }} />
        </div>
        <span className="text-sm text-ink-soft">{pct}%</span>
      </div>
    </div>
  );
}

export function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { reset } = useOnboarding();
  const { t } = useLanguage();
  const result = (location.state as { result?: PredictionResponse } | null)?.result;

  useEffect(() => {
    if (!result) {
      navigate("/onboarding", { replace: true });
    }
  }, [result, navigate]);

  if (!result) return null;

  const isAtRisk = result.prediction;
  const topFactors = result.top_factors.slice(0, 3);
  const maxAbs = Math.max(...topFactors.map((f) => Math.abs(f.contribution)), 1e-6);
  const riskPercent = Math.round(result.probability_depression * 100);

  const handleRetry = () => {
    reset();
    navigate("/onboarding");
  };

  return (
    <div className="flex min-h-screen flex-col">
      <Header variant="simple" />

      <main className="flex-1 px-6 py-10">
        <div className="mx-auto max-w-4xl">
          <div
            className={`rounded-[2.5rem] p-10 md:p-14 ${
              isAtRisk
                ? "bg-gradient-to-br from-peach-100 to-terracotta-300/40"
                : "bg-gradient-to-br from-sage-100 to-sage-50"
            }`}
          >
            <span
              className={`inline-flex rounded-full px-4 py-1.5 text-sm font-medium ${
                isAtRisk
                  ? "bg-surface/70 text-terracotta-800 dark:text-terracotta-300"
                  : "bg-surface/70 text-sage-700 dark:text-sage-300"
              }`}
            >
              {t.results.badge}
            </span>

            <h1 className="mt-6 max-w-lg font-heading text-4xl font-semibold text-ink">
              {isAtRisk ? t.results.riskTitle : t.results.okTitle}
            </h1>

            <p className="mt-5 max-w-xl text-ink-soft">{isAtRisk ? t.results.riskText : t.results.okText}</p>

            <p className="mt-4 text-sm text-ink-soft">
              {t.results.estimation(riskPercent, Math.round(result.confidence * 100))}
            </p>

            <div className="mt-8 flex flex-wrap gap-4">
              {isAtRisk ? (
                <Button variant="accent">
                  <PhoneIcon className="h-4 w-4" /> {t.results.needToTalk}
                </Button>
              ) : (
                <Button variant="primary">
                  <CheckIcon className="h-4 w-4" /> {t.results.continueExploring}
                </Button>
              )}
              <Button variant="outline" onClick={handleRetry}>
                {t.results.retakeTest}
              </Button>
            </div>
          </div>

          <section className="mt-14">
            <h2 className="text-center text-2xl font-semibold text-sage-700 dark:text-sage-300">
              {t.results.factorsTitle}
            </h2>
            <div className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-3">
              {topFactors.map((factor) => (
                <FactorCard key={factor.feature} factor={factor} maxAbs={maxAbs} t={t} />
              ))}
            </div>
          </section>

          {isAtRisk && (
            <section className="mt-14 rounded-[2.5rem] bg-cream-dark p-10 text-center md:p-14">
              <h2 className="text-2xl font-semibold text-ink">{t.results.notAloneTitle}</h2>
              <p className="mx-auto mt-3 max-w-xl text-ink-soft">{t.results.notAloneText}</p>
              <div className="mt-8 flex flex-wrap justify-center gap-4">
                <Button variant="primary">
                  <PhoneIcon className="h-4 w-4" /> {t.results.bookAppointment}
                </Button>
                <Button variant="outline">
                  <CompassIcon className="h-4 w-4" /> {t.results.discoverGuides}
                </Button>
              </div>
            </section>
          )}

          <p className="mx-auto mt-10 max-w-2xl text-center text-xs text-ink-soft">{t.results.disclaimer}</p>
        </div>
      </main>

      <Footer />
    </div>
  );
}
