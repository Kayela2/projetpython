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
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6 sm:py-5">
        <Link to="/" className="flex shrink-0 items-center gap-2 transition-opacity hover:opacity-80">
          <LeafIcon className="w-6 h-6 text-sage-700 dark:text-sage-300" />
          <span className="font-heading text-lg font-semibold text-sage-700 dark:text-sage-300 sm:text-xl">
            Serenity
          </span>
        </Link>

        <nav className="flex items-center gap-2 sm:gap-4 md:gap-6">
          <Link
            to="/"
            className="font-heading text-sm font-semibold text-ink transition-colors hover:text-sage-700 sm:text-base dark:hover:text-sage-300"
          >
            {t.header.home}
          </Link>
          <Link to="/#about" className="hidden text-ink-soft transition-colors hover:text-ink md:inline">
            {t.header.about}
          </Link>
          <LanguageToggle />
          <ThemeToggle />
          {variant === "full" && (
            <Link to="/onboarding" className="hidden sm:inline-flex">
              <Button variant="primary" className="px-5 py-2.5 text-sm">
                {t.header.signup}
              </Button>
            </Link>
          )}
        </nav>
      </div>
    </header>
  );
}
