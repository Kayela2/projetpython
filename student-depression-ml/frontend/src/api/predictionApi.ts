import type { OnboardingData, PredictionRequestPayload, PredictionResponse } from "../types/prediction";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

function toPayload(data: OnboardingData): PredictionRequestPayload {
  if (!data.gender || !data.department) {
    throw new Error("Formulaire incomplet: genre et département sont requis.");
  }
  return {
    age: data.age,
    gender: data.gender,
    department: data.department,
    cgpa: data.cgpa,
    sleep_duration: data.sleepDuration,
    study_hours: data.studyHours,
    social_media_hours: data.socialMediaHours,
    physical_activity: data.physicalActivity,
    stress_level: data.stressLevel,
  };
}

export async function predictDepression(data: OnboardingData): Promise<PredictionResponse> {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(toPayload(data)),
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new ApiError(body?.detail ?? "La prédiction a échoué.", response.status);
  }

  return response.json();
}
