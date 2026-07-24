import { describe, expect, it } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { OnboardingProvider, useOnboarding } from "./OnboardingContext";

function TestConsumer() {
  const { data, updateData, reset } = useOnboarding();
  return (
    <div>
      <span data-testid="stress">{data.stressLevel}</span>
      <span data-testid="gender">{data.gender ?? "none"}</span>
      <button onClick={() => updateData({ stressLevel: 9, gender: "Male" })}>update</button>
      <button onClick={reset}>reset</button>
    </div>
  );
}

describe("OnboardingContext", () => {
  it("provides default values and applies partial updates", () => {
    render(
      <OnboardingProvider>
        <TestConsumer />
      </OnboardingProvider>,
    );

    expect(screen.getByTestId("stress").textContent).toBe("5");
    expect(screen.getByTestId("gender").textContent).toBe("none");

    fireEvent.click(screen.getByText("update"));

    expect(screen.getByTestId("stress").textContent).toBe("9");
    expect(screen.getByTestId("gender").textContent).toBe("Male");
  });

  it("resets to the default values", () => {
    render(
      <OnboardingProvider>
        <TestConsumer />
      </OnboardingProvider>,
    );

    fireEvent.click(screen.getByText("update"));
    fireEvent.click(screen.getByText("reset"));

    expect(screen.getByTestId("stress").textContent).toBe("5");
    expect(screen.getByTestId("gender").textContent).toBe("none");
  });
});
