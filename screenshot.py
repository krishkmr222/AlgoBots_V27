import asyncio
from playwright.async_api import async_playwright

async def take_screenshot():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Navigate to the Flask app
        print("Navigating to http://localhost:5000")
        await page.goto("http://localhost:5000", wait_until="networkidle")
        
        # Take a screenshot
        print("Taking screenshot")
        await page.screenshot(path="landing_page.png", full_page=True)
        
        # Get page title
        title = await page.title()
        print(f"Page title: {title}")
        
        # Check for hero section
        hero_section = await page.query_selector(".hero-section")
        if hero_section:
            print("Found hero section")
        else:
            print("Could not find hero section")
        
        # Check for platform text
        platform_text = await page.query_selector(".platform-gradient-text")
        if platform_text:
            print("Found platform text")
        else:
            print("Could not find platform text")
        
        # Close the browser
        await browser.close()

if __name__ == "__main__":
    asyncio.run(take_screenshot())