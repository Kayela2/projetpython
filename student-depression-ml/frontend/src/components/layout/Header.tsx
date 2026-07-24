import { Link } from "react-router-dom";
import { LeafIcon } from "../ui/LeafIcon";
import { Button } from "../ui/Button";
import { ThemeToggle } from "../ui/ThemeToggle";
import { LanguageToggle } from "../ui/LanguageToggle";
import { useLanguage } from "../../context/LanguageContext";

interface HeaderProps {
  variant?: "full" | "simple";
}

export function Header({ variant = "full" }: HeaderProps) {
  const { t } = useLanguage();

  return (
    <header className="glass sticky top-0 z-50 w-full !border-x-0 !border-t-0 rounded-none">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
        <Link to="/" className="flex items-center gap-2 transition-opacity hover:opacity-80">
          <LeafIcon className="w-6 h-6 text-sage-700 dark:text-sage-300" />
          <span className="font-heading text-xl font-semibold text-sage-700 dark:text-sage-300">Serenity</span>
        </Link>

        {variant === "full" ? (
          <nav className="flex items-center gap-6">
            <Link to="/" className="font-heading font-semibold text-ink transition-colors hover:text-sage-700 dark:hover:text-sage-300">
              {t.header.home}
            </Link>
            <a href="#about" className="text-ink-soft transition-colors hover:text-ink">
              {t.header.about}
            </a>
            <LanguageToggle />
            <ThemeToggle />
            <Link to="/onboarding">
              <Button variant="primary" className="px-5 py-2.5 text-sm">
                {t.header.signup}
              </Button>
            </Link>
          </nav>
        ) : (
          <nav className="flex items-center gap-4">
            <a href="#about" className="text-ink-soft transition-colors hover:text-ink">
              {t.header.about}
            </a>
            <LanguageToggle />
            <ThemeToggle />
          </nav>
        )}
      </div>
    </header>
  );
}
