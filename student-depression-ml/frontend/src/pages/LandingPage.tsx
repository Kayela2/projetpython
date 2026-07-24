import { Link } from "react-router-dom";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { Button } from "../components/ui/Button";
import { BoltIcon, CheckIcon, HeartIcon, LockIcon, PlayIcon } from "../components/icons";
import { useLanguage } from "../context/LanguageContext";
import heroImage from "../assets/hero-meditation.png";
import pebbleImage from "../assets/pebble-sculpture.png";

const FEATURE_ICONS = [
  { icon: BoltIcon, iconBg: "bg-sage-100 text-sage-700 dark:text-sage-300" },
  { icon: LockIcon, iconBg: "bg-peach-100 text-terracotta-700 dark:text-terracotta-300" },
  { icon: HeartIcon, iconBg: "bg-lavender-100 text-lavender-600" },
];

export function LandingPage() {
  const { t } = useLanguage();
  const features = t.landing.features.map((f, i) => ({ ...f, ...FEATURE_ICONS[i] }));

  return (
    <div className="flex min-h-screen flex-col">
      <Header variant="full" />

      <main className="flex-1">
        {/* Hero */}
        <section className="mx-auto grid max-w-6xl grid-cols-1 items-center gap-12 px-6 py-10 md:grid-cols-2 md:py-16">
          <div>
            <span className="inline-flex items-center gap-2 rounded-full bg-surface px-4 py-1.5 text-sm text-ink-soft shadow-sm">
              {t.landing.badge}
            </span>
            <h1 className="mt-6 font-heading text-5xl font-semibold leading-tight text-ink md:text-6xl">
              {t.landing.heroTitleBefore}
              <span className="text-sage-600 dark:text-sage-300">{t.landing.heroTitleHighlight}</span>
              {t.landing.heroTitleAfter}
            </h1>
            <p className="mt-6 max-w-md text-lg text-ink-soft">{t.landing.heroSubtitle}</p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link to="/onboarding">
                <Button variant="primary">{t.landing.ctaStart}</Button>
              </Link>
              <Button variant="outline">
                <PlayIcon /> {t.landing.ctaDemo}
              </Button>
            </div>
          </div>

          <div className="relative">
            <div className="absolute -inset-6 -z-10 rounded-[2.5rem] bg-gradient-to-br from-sage-100 via-peach-100 to-transparent blur-2xl" />
            <div className="lift-hover overflow-hidden rounded-[2rem] shadow-xl dark:ring-1 dark:ring-white/10">
              <img
                src={heroImage}
                alt={t.landing.heroImageAlt}
                className="w-full object-cover transition-transform duration-500 ease-out hover:scale-105"
              />
            </div>
          </div>
        </section>

        {/* Why Serenity */}
        <section className="bg-cream-dark py-20">
          <div className="mx-auto max-w-6xl px-6 text-center">
            <h2 className="text-3xl font-semibold text-sage-700 dark:text-sage-300">{t.landing.featuresTitle}</h2>
            <p className="mt-3 text-ink-soft">{t.landing.featuresSubtitle}</p>

            <div className="mt-12 grid grid-cols-1 gap-6 md:grid-cols-3">
              {features.map((feature) => (
                <div key={feature.title} className="lift-hover rounded-3xl bg-surface p-8 text-left shadow-sm">
                  <span className={`inline-flex h-12 w-12 items-center justify-center rounded-full ${feature.iconBg}`}>
                    <feature.icon className="h-5 w-5" />
                  </span>
                  <h3 className="mt-5 text-xl font-semibold text-ink">{feature.title}</h3>
                  <p className="mt-2 text-ink-soft">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Aesthetic of calm */}
        <section id="about" className="mx-auto max-w-6xl px-6 py-20">
          <div className="grid grid-cols-1 items-center gap-10 rounded-[2.5rem] bg-cream-dark p-10 md:grid-cols-2 md:p-14">
            <div>
              <h2 className="text-3xl font-semibold text-ink">{t.landing.aestheticTitle}</h2>
              <p className="mt-4 text-ink-soft">{t.landing.aestheticText}</p>
              <ul className="mt-6 space-y-3">
                {t.landing.aestheticBullets.map((item) => (
                  <li key={item} className="flex items-center gap-3 text-ink-soft">
                    <CheckIcon className="h-5 w-5 text-sage-600 dark:text-sage-300" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
            <div className="lift-hover overflow-hidden rounded-3xl shadow-lg dark:ring-1 dark:ring-white/10">
              <img
                src={pebbleImage}
                alt={t.landing.aestheticImageAlt}
                className="w-full object-cover transition-transform duration-500 ease-out hover:scale-105"
              />
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="mx-auto max-w-3xl px-6 py-20 text-center">
          <h2 className="text-3xl font-semibold text-sage-700 dark:text-sage-300">{t.landing.finalCtaTitle}</h2>
          <p className="mt-4 text-ink-soft">{t.landing.finalCtaText}</p>
          <Link to="/onboarding" className="mt-8 inline-block">
            <Button variant="accent">{t.landing.finalCtaButton}</Button>
          </Link>
          <p className="mt-4 text-sm text-ink-soft">{t.landing.finalCtaFinePrint}</p>
        </section>
      </main>

      <Footer />
    </div>
  );
}
