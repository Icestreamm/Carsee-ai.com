const { test, expect } = require('@playwright/test');

test('اختبار موقع CarSee AI', async ({ page }) => {
  await page.goto('https://icestreamm.github.io/Carsee-ai.com/ar/index.html', { waitUntil: 'networkidle' });

  await expect(page).toHaveTitle(/CarSee/);
  await expect(page.locator('h1, h2').filter({ hasText: /فحص المركبات|CarSee/ })).toBeVisible();

  console.log('✅ الصفحة تحملت بنجاح');

  // مثال: التقاط صورة للصفحة كاملة
  await page.screenshot({ path: 'screenshot-full.png' });

  // مثال: الضغط على زر تنزيل (غير النص حسب زر موقعك)
  // await page.getByRole('button', { name: /تنزيل|ابدأ|احصل|Download/ }).click();
});