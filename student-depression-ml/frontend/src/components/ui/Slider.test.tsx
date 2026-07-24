import { describe, expect, it, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Slider } from "./Slider";

describe("Slider", () => {
  it("renders the label and formatted value", () => {
    render(
      <Slider label="Heures d'étude" value={4.5} min={0} max={12} unit="h" onChange={() => {}} />,
    );

    expect(screen.getByText("Heures d'étude")).toBeInTheDocument();
    expect(screen.getByText("4.5h")).toBeInTheDocument();
  });

  it("calls onChange with a number when moved", () => {
    const onChange = vi.fn();
    render(<Slider label="Stress" value={5} min={1} max={10} onChange={onChange} />);

    const input = screen.getByRole("slider");
    fireEvent.change(input, { target: { value: "8" } });

    expect(onChange).toHaveBeenCalledWith(8);
  });
});
