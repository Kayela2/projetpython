/**
 * End-to-end smoke test for the full onboarding -> prediction flow.
 *
 * Prerequisites (not started by this script):
 *   - Backend running at http://localhost:8000 (uvicorn app.main:app)
 *   - Frontend dev server running at http://localhost:5173 (npm run dev)
 *
 * Usage: npm run test:e2e
 */
import { chromium } from "playwright";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SHOT_DIR = path.join(__dirname, "screenshots");
const APP_URL = process.env.E2E_APP_URL ?? "http://localhost:5173";

fs.mkdirSync(SHOT_DIR, { recursive: true });

const consoleErrors = [];

async function main() {
  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });
  page.on("pageerror", (err) => consoleErrors.push(`PAGEERROR: ${err.message}`));

  const shot = (name) => page.screenshot({ path: path.join(SHOT_DIR, `${name}.png`), fullPage: true });

  // 1. Landing page
  await page.goto(APP_URL, { waitUntil: "networkidle" });
  await page.waitForSelector("text=Prends un");
  await shot("01_landing");

  // 2. Enter onboarding
  await page.click("text=Commencer");
  await page.waitForSelector("text=Commençons par vous");

  // Step 1: Profil
  await page.click("button:has-text('Femme')");
  await page.click("button:has-text('Science')");
  await shot("02_step1_profile");
  await page.click("button:has-text('Continuer')");

  // Step 2: Academics
  await page.waitForSelector("text=Equilibre de Vie");
  await shot("03_step2_academics");
  await page.click("button:has-text('Continuer')");

  // Step 3: Lifestyle
  await page.waitForSelector("text=Votre Style de Vie");
  await shot("04_step3_lifestyle");
  await page.click("button:has-text('Continuer')");

  // Step 4: Feelings — push stress high for a deterministic, interesting case
  await page.waitForSelector("text=Votre Ressenti");
  await page.locator("input[type=range]").last().fill("9");
  await shot("05_step4_feelings");
  await page.click("text=Terminer l'analyse");

  // Loading -> Results
  await page.waitForURL("**/loading");
  await shot("06_loading");

  await page.waitForURL("**/results", { timeout: 15000 });
  await page.waitForSelector("text=Votre Bilan");
  await shot("07_results");

  // Assertions: page content is internally consistent (regression test for the
  // prediction/probability mismatch bug found during manual QA)
  const bodyText = await page.textContent("body");
  assert.match(bodyText, /probabilité associée à des signes de dépression/, "results page should show the model probability");

  const isAtRisk = bodyText.includes("Quelques signaux à surveiller");
  const isReassuring = bodyText.includes("Vous semblez sur la bonne voie");
  assert.ok(isAtRisk || isReassuring, "results page should render one of the two known headlines");

  const probabilityMatch = bodyText.match(/(\d+)%\s*de probabilité/);
  assert.ok(probabilityMatch, "probability percentage should be present in the results text");
  const probability = Number(probabilityMatch[1]);
  if (isAtRisk) {
    assert.ok(probability >= 50, `expected probability >= 50 for the at-risk headline, got ${probability}`);
  } else {
    assert.ok(probability < 50, `expected probability < 50 for the reassuring headline, got ${probability}`);
  }

  assert.deepEqual(consoleErrors, [], "no console errors should be raised during the flow");

  await browser.close();
  console.log("E2E OK — all assertions passed. Screenshots in", SHOT_DIR);
}

main().catch((err) => {
  console.error("E2E FAILED:", err.message);
  if (consoleErrors.length) console.error("Console errors captured:", consoleErrors);
  process.exit(1);
});
