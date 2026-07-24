import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./context/ThemeContext";
import { LanguageProvider } from "./context/LanguageContext";
import { OnboardingProvider } from "./context/OnboardingContext";
import { BackgroundDecor } from "./components/layout/BackgroundDecor";
import { LandingPage } from "./pages/LandingPage";
import { OnboardingPage } from "./pages/OnboardingPage";
import { LoadingPage } from "./pages/LoadingPage";
import { ResultsPage } from "./pages/ResultsPage";

function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <BrowserRouter>
          <OnboardingProvider>
            <BackgroundDecor />
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/onboarding" element={<OnboardingPage />} />
              <Route path="/loading" element={<LoadingPage />} />
              <Route path="/results" element={<ResultsPage />} />
            </Routes>
          </OnboardingProvider>
        </BrowserRouter>
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App;
