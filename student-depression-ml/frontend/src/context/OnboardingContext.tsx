import { createContext, useContext, useState, type ReactNode } from "react";
import type { OnboardingData } from "../types/prediction";

const DEFAULT_DATA: OnboardingData = {
  age: 21,
  gender: null,
  department: null,
  cgpa: 2.9,
  studyHours: 4.5,
  sleepDuration: 7,
  socialMediaHours: 3.5,
  physicalActivity: 60,
  stressLevel: 5,
};

interface OnboardingContextValue {
  data: OnboardingData;
  updateData: (patch: Partial<OnboardingData>) => void;
  reset: () => void;
}

const OnboardingContext = createContext<OnboardingContextValue | undefined>(undefined);

export function OnboardingProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<OnboardingData>(DEFAULT_DATA);

  const updateData = (patch: Partial<OnboardingData>) => {
    setData((prev) => ({ ...prev, ...patch }));
  };

  const reset = () => setData(DEFAULT_DATA);

  return (
    <OnboardingContext.Provider value={{ data, updateData, reset }}>
      {children}
    </OnboardingContext.Provider>
  );
}

// oxlint-disable-next-line react/only-export-components -- Provider + hook co-located is the standard React context pattern
export function useOnboarding(): OnboardingContextValue {
  const ctx = useContext(OnboardingContext);
  if (!ctx) {
    throw new Error("useOnboarding must be used within an OnboardingProvider");
  }
  return ctx;
}
