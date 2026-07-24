import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { ApiError, predictDepression } from "./predictionApi";
import type { OnboardingData } from "../types/prediction";

const COMPLETE_DATA: OnboardingData = {
  age: 21,
  gender: "Female",
  department: "Science",
  cgpa: 2.9,
  studyHours: 5,
  sleepDuration: 6.5,
  socialMediaHours: 4,
  physicalActivity: 60,
  stressLevel: 7,
};

describe("predictDepression", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("maps camelCase onboarding data to the snake_case API payload", async () => {
    const mockResponse = { prediction: false };
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      json: async () => mockResponse,
    });

    await predictDepression(COMPLETE_DATA);

    const [, options] = (fetch as ReturnType<typeof vi.fn>).mock.calls[0];
    const body = JSON.parse(options.body as string);
    expect(body).toEqual({
      age: 21,
      gender: "Female",
      department: "Science",
      cgpa: 2.9,
      sleep_duration: 6.5,
      study_hours: 5,
      social_media_hours: 4,
      physical_activity: 60,
      stress_level: 7,
    });
  });

  it("throws an ApiError with the server-provided detail on non-2xx responses", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: false,
      status: 422,
      json: async () => ({ detail: "Données invalides." }),
    });

    await expect(predictDepression(COMPLETE_DATA)).rejects.toMatchObject(
      new ApiError("Données invalides.", 422),
    );
  });

  it("throws before calling fetch when gender or department is missing", async () => {
    const incomplete: OnboardingData = { ...COMPLETE_DATA, gender: null };

    await expect(predictDepression(incomplete)).rejects.toThrow(/incomplet/i);
    expect(fetch).not.toHaveBeenCalled();
  });
});
