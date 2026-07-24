export type Gender = "Female" | "Male";
export type Department = "Science" | "Engineering" | "Medical" | "Arts" | "Business";

export interface OnboardingData {
  age: number;
  gender: Gender | null;
  department: Department | null;
  cgpa: number;
  studyHours: number;
  sleepDuration: number;
  socialMediaHours: number;
  physicalActivity: number;
  stressLevel: number;
}

export interface PredictionRequestPayload {
  age: number;
  gender: Gender;
  department: Department;
  cgpa: number;
  sleep_duration: number;
  study_hours: number;
  social_media_hours: number;
  physical_activity: number;
  stress_level: number;
}

export type FactorDirection = "increases_risk" | "decreases_risk" | "neutral";

export interface FeatureContribution {
  feature: string;
  label: string;
  value: string;
  contribution: number;
  direction: FactorDirection;
}

export interface PredictionResponse {
  prediction: boolean;
  prediction_label: string;
  probability_depression: number;
  probability_not_depression: number;
  confidence: number;
  top_factors: FeatureContribution[];
  model_version: string;
}
