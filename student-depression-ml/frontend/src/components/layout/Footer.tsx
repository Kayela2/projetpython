import { useLanguage } from "../../context/LanguageContext";

export function Footer() {
  const { t } = useLanguage();

  return (
    <footer className="w-full border-t border-ink/10 mt-auto">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-6 py-8 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="font-heading text-lg font-semibold text-sage-700 dark:text-sage-300">Serenity</p>
          <p className="text-sm text-ink-soft">{t.footer.tagline}</p>
        </div>
        <div className="flex gap-6 text-sm text-ink-soft">
          <span>{t.footer.privacy}</span>
          <span>{t.footer.terms}</span>
          <span>{t.footer.support}</span>
        </div>
      </div>
    </footer>
  );
}
