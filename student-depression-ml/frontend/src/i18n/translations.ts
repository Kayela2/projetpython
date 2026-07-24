/** Central translation dictionary. Add a new language by adding a key here
 * and filling in every field — TypeScript will flag anything missing since
 * both languages share the same `Translations` shape. */

export interface Translations {
  header: {
    home: string;
    about: string;
    signup: string;
  };
  themeToggle: {
    toLight: string;
    toDark: string;
  };
  languageToggle: {
    label: string;
  };
  footer: {
    tagline: string;
    privacy: string;
    terms: string;
    support: string;
  };
  landing: {
    badge: string;
    heroTitleBefore: string;
    heroTitleHighlight: string;
    heroTitleAfter: string;
    heroSubtitle: string;
    ctaStart: string;
    ctaDemo: string;
    heroImageAlt: string;
    featuresTitle: string;
    featuresSubtitle: string;
    features: { title: string; description: string }[];
    aestheticTitle: string;
    aestheticText: string;
    aestheticBullets: string[];
    aestheticImageAlt: string;
    finalCtaTitle: string;
    finalCtaText: string;
    finalCtaButton: string;
    finalCtaFinePrint: string;
  };
  onboarding: {
    stepLabel: (step: number, total: number) => string;
    previous: string;
    back: string;
    continueBtn: string;
    finish: string;
    analyzing: string;
  };
  stepProfile: {
    title: string;
    subtitle: string;
    ageQuestion: string;
    ageUnit: string;
    ageMinLabel: string;
    ageMaxLabel: string;
    genderQuestion: string;
    departmentQuestion: string;
  };
  gender: {
    female: string;
    male: string;
  };
  departments: {
    Science: string;
    Engineering: string;
    Arts: string;
    Medical: string;
    Business: string;
  };
  stepAcademics: {
    title: string;
    subtitle: string;
    cgpaLabel: string;
    studyHoursLabel: string;
    studyHoursMin: string;
    studyHoursMax: string;
  };
  stepLifestyle: {
    imageAlt: string;
    imageCaption: string;
    imageText: string;
    title: string;
    sleepLabel: string;
    sleepMin: string;
    sleepMax: string;
    socialLabel: string;
    socialUnit: string;
    socialMin: string;
    socialMax: string;
    activityLabel: string;
    activityUnit: string;
    activityMin: string;
    activityMax: string;
  };
  stepFeelings: {
    title: string;
    subtitle: string;
    calm: string;
    exhausted: string;
    quote: string;
  };
  loading: {
    imageAlt: string;
    steps: string[];
    errorBadge: string;
    errorTitle: string;
    genericError: string;
    errorHint: string;
    errorButton: string;
    analyzingBadge: string;
    title: string;
    subtitle: string;
  };
  results: {
    badge: string;
    riskTitle: string;
    okTitle: string;
    riskText: string;
    okText: string;
    estimation: (percent: number, confidence: number) => string;
    needToTalk: string;
    continueExploring: string;
    retakeTest: string;
    factorsTitle: string;
    factorValueLabel: string;
    increasesRisk: string;
    decreasesRisk: string;
    neutralImpact: string;
    notAloneTitle: string;
    notAloneText: string;
    bookAppointment: string;
    discoverGuides: string;
    disclaimer: string;
  };
  featureLabels: Record<string, string>;
}

const fr: Translations = {
  header: {
    home: "Accueil",
    about: "À propos",
    signup: "S'inscrire",
  },
  themeToggle: {
    toLight: "Passer au thème clair",
    toDark: "Passer au thème sombre",
  },
  languageToggle: {
    label: "Changer de langue",
  },
  footer: {
    tagline: "© 2026 Serenity. Vous vous en sortez très bien.",
    privacy: "Confidentialité",
    terms: "Conditions",
    support: "Support",
  },
  landing: {
    badge: "✦ Élu application de l'année",
    heroTitleBefore: "Prends un ",
    heroTitleHighlight: "moment",
    heroTitleAfter: " pour toi",
    heroSubtitle:
      "Retrouvez votre calme intérieur grâce à des exercices de respiration guidés et une méditation adaptée à votre rythme de vie.",
    ctaStart: "Commencer",
    ctaDemo: "Démo",
    heroImageAlt: "Femme sereine assise près d'une fenêtre avec une tasse de thé",
    featuresTitle: "Pourquoi choisir Serenity ?",
    featuresSubtitle: "Une approche douce pour un bien-être durable.",
    features: [
      {
        title: "Rapide",
        description:
          "Des sessions de 2 à 5 minutes conçues pour s'intégrer parfaitement dans vos journées les plus chargées.",
      },
      {
        title: "Privé",
        description:
          "Vos données et votre progression restent uniquement sur votre appareil. Pas de cloud, pas de partage.",
      },
      {
        title: "Bienveillant",
        description:
          "Une interface sans notifications agressives ni culpabilité. Nous sommes là quand vous en avez besoin.",
      },
    ],
    aestheticTitle: "L'esthétique du calme",
    aestheticText:
      "Nous croyons que le design est le premier pas vers la sérénité. Notre interface s'inspire des textures naturelles et des couleurs apaisantes de l'aube.",
    aestheticBullets: ["Palette chromatique relaxante", "Micro-interactions organiques", "Zéro distraction visuelle"],
    aestheticImageAlt: "Sculpture galet aux couleurs pastel sur une table en bois",
    finalCtaTitle: "Prêt à respirer ?",
    finalCtaText: "Rejoignez des milliers de personnes qui ont déjà transformé leur quotidien avec Serenity.",
    finalCtaButton: "Découvrir Serenity",
    finalCtaFinePrint: "Gratuit pendant 14 jours • Sans engagement",
  },
  onboarding: {
    stepLabel: (step, total) => `Étape ${step} sur ${total}`,
    previous: "Précédent",
    back: "Retour",
    continueBtn: "Continuer",
    finish: "Terminer l'analyse",
    analyzing: "Analyse...",
  },
  stepProfile: {
    title: "Commençons par vous",
    subtitle: "Aidez-nous à personnaliser votre expérience de bien-être en quelques questions.",
    ageQuestion: "Quel est votre âge ?",
    ageUnit: " ans",
    ageMinLabel: "18 ans",
    ageMaxLabel: "24 ans",
    genderQuestion: "Quel est votre genre ?",
    departmentQuestion: "Votre département d'études",
  },
  gender: {
    female: "Femme",
    male: "Homme",
  },
  departments: {
    Science: "Science",
    Engineering: "Ingénierie",
    Arts: "Arts",
    Medical: "Médecine",
    Business: "Business",
  },
  stepAcademics: {
    title: "Equilibre de Vie",
    subtitle: "Parlez-nous de votre quotidien académique pour que nous puissions adapter vos séances.",
    cgpaLabel: "Moyenne générale (CGPA)",
    studyHoursLabel: "Heures d'étude par jour",
    studyHoursMin: "0h",
    studyHoursMax: "12h",
  },
  stepLifestyle: {
    imageAlt: "Bureau en bois avec carnet, tasse de café et plante près d'une fenêtre",
    imageCaption: "Équilibre & Clarté",
    imageText:
      "Vos habitudes quotidiennes sont le fondement de votre bien-être. Prenez un instant pour refléter votre réalité.",
    title: "Votre Style de Vie",
    sleepLabel: "Sommeil",
    sleepMin: "Repos limité",
    sleepMax: "Optimisé",
    socialLabel: "Réseaux Sociaux",
    socialUnit: "h/j",
    socialMin: "Digital Detox",
    socialMax: "Connecté",
    activityLabel: "Activité Physique",
    activityUnit: " min",
    activityMin: "Sédentaire",
    activityMax: "Athlétique",
  },
  stepFeelings: {
    title: "Votre Ressenti",
    subtitle:
      "Prenez un moment pour écouter votre corps. Comment évalueriez-vous votre niveau de stress en cet instant précis ?",
    calm: "Serein",
    exhausted: "Épuisé",
    quote: "«Un voyage de mille lieues commence par un seul pas.»",
  },
  loading: {
    imageAlt: "Sculpture apaisante en cours de préparation",
    steps: [
      "Analyse de votre profil...",
      "Calibrage du modèle Kernel SVM...",
      "Optimisation des fréquences...",
      "Préparation de votre bilan...",
    ],
    errorBadge: "● Erreur",
    errorTitle: "L'analyse n'a pas pu aboutir",
    genericError: "Une erreur est survenue.",
    errorHint: "Vérifiez que le serveur de l'API (backend FastAPI) est bien démarré.",
    errorButton: "Retour au questionnaire",
    analyzingBadge: "● ANALYSE EN COURS...",
    title: "Nous façonnons votre espace de calme.",
    subtitle:
      "Prenez un instant pour respirer pendant que nous préparons votre bilan personnel. La sérénité commence ici.",
  },
  results: {
    badge: "Votre Bilan",
    riskTitle: "Quelques signaux à surveiller",
    okTitle: "Vous semblez sur la bonne voie",
    riskText:
      "Prendre conscience de son état est la première étape vers l'apaisement. Vos réponses suggèrent que votre équilibre actuel est fragilisé par une accumulation de tensions. Ce n'est pas une fatalité, mais une invitation à ralentir.",
    okText:
      "Vos réponses ne font pas apparaître de signaux d'alerte marquants aujourd'hui. Continuez à prendre soin de votre équilibre — sommeil, activité physique et temps de repos restent vos meilleurs alliés.",
    estimation: (percent, confidence) =>
      `Estimation du modèle : ${percent}% de probabilité associée à des signes de dépression (confiance du modèle : ${confidence}%).`,
    needToTalk: "Besoin de parler ?",
    continueExploring: "Continuer à explorer Serenity",
    retakeTest: "Refaire le test",
    factorsTitle: "Facteurs observés",
    factorValueLabel: "Valeur renseignée",
    increasesRisk: "contribue à augmenter le risque estimé.",
    decreasesRisk: "contribue à réduire le risque estimé.",
    neutralImpact: "impact neutre sur l'estimation.",
    notAloneTitle: "Ne restez pas seul(e) avec ces pensées",
    notAloneText:
      "Parler à un professionnel peut vous aider à dénouer ces tensions et à retrouver votre sérénité habituelle. Nos praticiens sont à votre écoute 24/7.",
    bookAppointment: "Prendre rendez-vous",
    discoverGuides: "Découvrir nos guides",
    disclaimer:
      "Ce résultat est généré par un modèle statistique (Kernel SVM) à des fins pédagogiques et ne constitue en aucun cas un diagnostic médical. En cas de détresse, contactez un professionnel de santé.",
  },
  featureLabels: {
    Age: "Âge",
    CGPA: "Moyenne générale (CGPA)",
    Sleep_Duration: "Durée de sommeil",
    Study_Hours: "Heures d'étude",
    Social_Media_Hours: "Heures sur les réseaux sociaux",
    Physical_Activity: "Activité physique",
    Stress_Level: "Niveau de stress",
    Gender: "Genre",
    Department: "Département",
  },
};

const en: Translations = {
  header: {
    home: "Home",
    about: "About",
    signup: "Sign up",
  },
  themeToggle: {
    toLight: "Switch to light theme",
    toDark: "Switch to dark theme",
  },
  languageToggle: {
    label: "Change language",
  },
  footer: {
    tagline: "© 2026 Serenity. You're doing great.",
    privacy: "Privacy",
    terms: "Terms",
    support: "Support",
  },
  landing: {
    badge: "✦ App of the year",
    heroTitleBefore: "Take a ",
    heroTitleHighlight: "moment",
    heroTitleAfter: " for yourself",
    heroSubtitle: "Find your inner calm with guided breathing exercises and meditation tailored to your pace of life.",
    ctaStart: "Get started",
    ctaDemo: "Watch demo",
    heroImageAlt: "Serene woman sitting by a window with a cup of tea",
    featuresTitle: "Why choose Serenity?",
    featuresSubtitle: "A gentle approach to lasting well-being.",
    features: [
      {
        title: "Quick",
        description: "2 to 5 minute sessions designed to fit seamlessly into your busiest days.",
      },
      {
        title: "Private",
        description: "Your data and progress stay on your device. No cloud, no sharing.",
      },
      {
        title: "Kind",
        description: "An interface with no aggressive notifications or guilt-tripping. We're here when you need us.",
      },
    ],
    aestheticTitle: "The aesthetics of calm",
    aestheticText:
      "We believe design is the first step toward serenity. Our interface draws on natural textures and the soothing colors of dawn.",
    aestheticBullets: ["Relaxing color palette", "Organic micro-interactions", "Zero visual distraction"],
    aestheticImageAlt: "Pastel-colored pebble sculpture on a wooden table",
    finalCtaTitle: "Ready to breathe?",
    finalCtaText: "Join thousands of people who have already transformed their daily lives with Serenity.",
    finalCtaButton: "Discover Serenity",
    finalCtaFinePrint: "Free for 14 days • No commitment",
  },
  onboarding: {
    stepLabel: (step, total) => `Step ${step} of ${total}`,
    previous: "Previous",
    back: "Back",
    continueBtn: "Continue",
    finish: "Finish analysis",
    analyzing: "Analyzing...",
  },
  stepProfile: {
    title: "Let's start with you",
    subtitle: "Help us personalize your well-being experience with a few questions.",
    ageQuestion: "How old are you?",
    ageUnit: " yrs",
    ageMinLabel: "18 yrs",
    ageMaxLabel: "24 yrs",
    genderQuestion: "What's your gender?",
    departmentQuestion: "Your field of study",
  },
  gender: {
    female: "Female",
    male: "Male",
  },
  departments: {
    Science: "Science",
    Engineering: "Engineering",
    Arts: "Arts",
    Medical: "Medicine",
    Business: "Business",
  },
  stepAcademics: {
    title: "Life Balance",
    subtitle: "Tell us about your academic routine so we can tailor your sessions.",
    cgpaLabel: "GPA (CGPA)",
    studyHoursLabel: "Study hours per day",
    studyHoursMin: "0h",
    studyHoursMax: "12h",
  },
  stepLifestyle: {
    imageAlt: "Wooden desk with a notebook, coffee cup, and plant near a window",
    imageCaption: "Balance & Clarity",
    imageText: "Your daily habits are the foundation of your well-being. Take a moment to reflect your reality.",
    title: "Your Lifestyle",
    sleepLabel: "Sleep",
    sleepMin: "Limited rest",
    sleepMax: "Optimal",
    socialLabel: "Social Media",
    socialUnit: "h/day",
    socialMin: "Digital detox",
    socialMax: "Connected",
    activityLabel: "Physical Activity",
    activityUnit: " min",
    activityMin: "Sedentary",
    activityMax: "Athletic",
  },
  stepFeelings: {
    title: "How You Feel",
    subtitle: "Take a moment to listen to your body. How would you rate your stress level right now?",
    calm: "Calm",
    exhausted: "Exhausted",
    quote: "“A journey of a thousand miles begins with a single step.”",
  },
  loading: {
    imageAlt: "Soothing sculpture being prepared",
    steps: [
      "Analyzing your profile...",
      "Calibrating the Kernel SVM model...",
      "Tuning the frequencies...",
      "Preparing your report...",
    ],
    errorBadge: "● Error",
    errorTitle: "The analysis couldn't be completed",
    genericError: "An error occurred.",
    errorHint: "Make sure the API server (FastAPI backend) is running.",
    errorButton: "Back to the questionnaire",
    analyzingBadge: "● ANALYZING...",
    title: "We're shaping your space of calm.",
    subtitle: "Take a moment to breathe while we prepare your personal report. Serenity starts here.",
  },
  results: {
    badge: "Your Report",
    riskTitle: "A few signals worth watching",
    okTitle: "You seem to be on the right track",
    riskText:
      "Becoming aware of how you feel is the first step toward relief. Your answers suggest your current balance is strained by a buildup of tension. It isn't inevitable — it's an invitation to slow down.",
    okText:
      "Your answers don't show any major warning signs today. Keep taking care of your balance — sleep, physical activity, and rest remain your best allies.",
    estimation: (percent, confidence) =>
      `Model estimate: ${percent}% probability associated with signs of depression (model confidence: ${confidence}%).`,
    needToTalk: "Need to talk?",
    continueExploring: "Keep exploring Serenity",
    retakeTest: "Retake the test",
    factorsTitle: "Observed factors",
    factorValueLabel: "Reported value",
    increasesRisk: "contributes to increasing the estimated risk.",
    decreasesRisk: "contributes to reducing the estimated risk.",
    neutralImpact: "neutral impact on the estimate.",
    notAloneTitle: "You don't have to face this alone",
    notAloneText:
      "Talking to a professional can help you ease this tension and find your usual sense of calm. Our practitioners are available 24/7.",
    bookAppointment: "Book an appointment",
    discoverGuides: "Discover our guides",
    disclaimer:
      "This result is generated by a statistical model (Kernel SVM) for educational purposes and is in no way a medical diagnosis. If you're in distress, please contact a healthcare professional.",
  },
  featureLabels: {
    Age: "Age",
    CGPA: "GPA (CGPA)",
    Sleep_Duration: "Sleep duration",
    Study_Hours: "Study hours",
    Social_Media_Hours: "Social media hours",
    Physical_Activity: "Physical activity",
    Stress_Level: "Stress level",
    Gender: "Gender",
    Department: "Department",
  },
};

export const translations = { fr, en };
