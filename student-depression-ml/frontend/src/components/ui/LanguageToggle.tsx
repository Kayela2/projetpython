import { useLanguage } from "../../context/LanguageContext";

export function LanguageToggle() {
  const { language, toggleLanguage, t } = useLanguage();

  return (
    <button
      type="button"
      onClick={toggleLanguage}
      aria-label={t.languageToggle.label}
      title={t.languageToggle.label}
      className="flex h-9 items-center justify-center gap-1 rounded-full bg-sage-50 px-3 text-xs font-heading font-bold text-sage-700 transition-all duration-200 hover:scale-105 hover:bg-sage-100 hover:shadow-md active:scale-95 dark:text-sage-300"
    >
      <span className={language === "fr" ? "opacity-100" : "opacity-40"}>FR</span>
      <span className="opacity-40">/</span>
      <span className={language === "en" ? "opacity-100" : "opacity-40"}>EN</span>
    </button>
  );
}
