import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { ProgressBar } from "../components/ui/ProgressBar";
import { Spinner } from "../components/ui/Spinner";
import { Button } from "../components/ui/Button";
import { useOnboarding } from "../context/OnboardingContext";
import { useLanguage } from "../context/LanguageContext";
import { predictDepression } from "../api/predictionApi";
import pebbleImage from "../assets/pebble-sculpture.png";

export function LoadingPage() {
  const { data } = useOnboarding();
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [percent, setPercent] = useState(4);
  const [error, setError] = useState<string | null>(null);
  const startedRef = useRef(false);

  useEffect(() => {
    if (!data.gender || !data.department) {
      navigate("/onboarding", { replace: true });
    }
  }, [data, navigate]);

  useEffect(() => {
    const interval = setInterval(() => {
      setPercent((p) => (p < 90 ? p + Math.random() * 8 : p));
    }, 350);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Guards against React 18 StrictMode's dev-only double-invoke of effects:
    // startedRef persists across the synthetic mount/cleanup/remount, so the
    // fetch itself only ever fires once and is left to run to completion
    // (a cleanup-based cancellation flag would wrongly abort it, since the
    // cleanup from the first invocation fires before the second one runs).
    if (startedRef.current) return;
    startedRef.current = true;

    async function run() {
      try {
        const [result] = await Promise.all([
          predictDepression(data),
          new Promise((resolve) => setTimeout(resolve, 1800)),
        ]);
        setPercent(100);
        setTimeout(() => navigate("/results", { state: { result } }), 400);
      } catch (err) {
        setError(err instanceof Error ? err.message : t.loading.genericError);
      }
    }

    run();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data, navigate]);

  const steps = t.loading.steps;
  const stepLabel = steps[Math.min(steps.length - 1, Math.floor(percent / 25))];

  return (
    <div className="flex min-h-screen flex-col">
      <Header variant="simple" />

      <main className="flex flex-1 items-center justify-center px-6 py-10">
        <div className="mx-auto max-w-xl text-center">
          <div className="relative mx-auto flex h-64 w-64 items-center justify-center">
            {!error && (
              <Spinner
                size={280}
                className="absolute border-sage-100/70 border-t-terracotta-700 duration-1000"
              />
            )}
            <img
              src={pebbleImage}
              alt={t.loading.imageAlt}
              className="h-64 w-64 rounded-full object-cover shadow-lg dark:ring-1 dark:ring-white/10"
            />
          </div>

          {error ? (
            <>
              <span className="mt-8 inline-flex items-center gap-2 rounded-full bg-terracotta-100 px-4 py-1.5 text-sm font-medium text-terracotta-800 dark:text-terracotta-300">
                {t.loading.errorBadge}
              </span>
              <h1 className="mt-6 font-heading text-3xl font-semibold text-ink">{t.loading.errorTitle}</h1>
              <p className="mt-4 text-ink-soft">{error}</p>
              <p className="mt-1 text-sm text-ink-soft">{t.loading.errorHint}</p>
              <Button className="mt-8" variant="primary" onClick={() => navigate("/onboarding")}>
                {t.loading.errorButton}
              </Button>
            </>
          ) : (
            <>
              <span className="mt-8 inline-flex items-center gap-2 rounded-full bg-sage-50 px-4 py-1.5 text-sm font-medium text-sage-700 dark:text-sage-300">
                {t.loading.analyzingBadge}
              </span>
              <h1 className="mt-6 font-heading text-3xl font-semibold text-ink md:text-4xl">{t.loading.title}</h1>
              <p className="mt-4 text-ink-soft">{t.loading.subtitle}</p>

              <div className="mx-auto mt-10 max-w-sm">
                <ProgressBar percent={percent} colorClassName="bg-terracotta-700" />
                <div className="mt-2 flex justify-between text-sm text-ink-soft">
                  <span>{stepLabel}</span>
                  <span>{Math.round(percent)}%</span>
                </div>
              </div>
            </>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}
