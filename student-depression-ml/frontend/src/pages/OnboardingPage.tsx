import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { ProgressBar } from "../components/ui/ProgressBar";
import { Spinner } from "../components/ui/Spinner";
import { ArrowLeftIcon, ArrowRightIcon } from "../components/icons";
import { useOnboarding } from "../context/OnboardingContext";
import { useLanguage } from "../context/LanguageContext";
import { StepProfile } from "../components/onboarding/StepProfile";
import { StepAcademics } from "../components/onboarding/StepAcademics";
import { StepLifestyle } from "../components/onboarding/StepLifestyle";
import { StepFeelings } from "../components/onboarding/StepFeelings";

const TOTAL_STEPS = 4;

export function OnboardingPage() {
  const [step, setStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { data } = useOnboarding();
  const { t } = useLanguage();
  const navigate = useNavigate();

  const isStep1Valid = data.gender !== null && data.department !== null;
  const canGoNext = step !== 1 || isStep1Valid;

  const goNext = () => {
    if (!canGoNext) return;
    if (step === TOTAL_STEPS) {
      setIsSubmitting(true);
      navigate("/loading");
      return;
    }
    setStep((s) => s + 1);
  };

  const goBack = () => {
    if (step === 1) {
      navigate("/");
      return;
    }
    setStep((s) => s - 1);
  };

  return (
    <div className="flex min-h-screen flex-col">
      <Header variant="simple" />

      <main className="flex-1 px-6 py-6">
        <div className="mx-auto max-w-3xl">
          <div className="mb-8 flex items-center justify-between text-sm text-ink-soft">
            <span className="font-heading font-semibold text-terracotta-700 dark:text-terracotta-300">
              {t.onboarding.stepLabel(step, TOTAL_STEPS)}
            </span>
            <span>{Math.round((step / TOTAL_STEPS) * 100)}%</span>
          </div>
          <ProgressBar percent={(step / TOTAL_STEPS) * 100} />

          <Card variant="glass" className="mt-8 p-8 md:p-12">
            {step === 1 && <StepProfile />}
            {step === 2 && <StepAcademics />}
            {step === 3 && <StepLifestyle />}
            {step === 4 && <StepFeelings />}

            <div className="mt-12 flex items-center justify-between border-t border-ink/10 pt-8">
              <Button variant="ghost" onClick={goBack} disabled={isSubmitting}>
                <ArrowLeftIcon /> {step === 1 ? t.onboarding.previous : t.onboarding.back}
              </Button>
              <Button
                variant={step === TOTAL_STEPS ? "primary" : "accent"}
                onClick={goNext}
                disabled={!canGoNext || isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <Spinner size={18} className="border-white/30 border-t-white" /> {t.onboarding.analyzing}
                  </>
                ) : (
                  <>
                    {step === TOTAL_STEPS ? t.onboarding.finish : t.onboarding.continueBtn}
                    {step !== TOTAL_STEPS && <ArrowRightIcon />}
                  </>
                )}
              </Button>
            </div>
          </Card>
        </div>
      </main>

      <Footer />
    </div>
  );
}
