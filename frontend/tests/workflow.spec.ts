import { test, expect } from "@playwright/test";

test("home page shows workflow entry", async ({ page }) => {
    await page.goto("http://127.0.0.1:5173");
    await expect(page.getByText("Start Simulation")).toBeVisible();
});
