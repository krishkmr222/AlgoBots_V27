import asyncio
from playwright.async_api import async_playwright
import json

async def test_ui_changes():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Navigate to the Flask app
        print("Navigating to http://localhost:5000")
        await page.goto("http://localhost:5000", wait_until="networkidle")
        
        # Take a screenshot of the hero section
        print("Taking screenshot of hero section")
        hero_section = await page.query_selector(".hero-section")
        if hero_section:
            await hero_section.screenshot(path="hero_section.png")
            print("✅ Hero section screenshot saved")
        else:
            print("❌ Could not find hero section")
            return
        
        # Check if "Algo Trading Platform" text has the correct gradient
        platform_text = await page.query_selector(".platform-gradient-text")
        if platform_text:
            # Get the computed style for the platform text
            gradient_style = await page.evaluate("""() => {
                const element = document.querySelector('.platform-gradient-text');
                const style = window.getComputedStyle(element);
                return {
                    background: style.background,
                    backgroundImage: style.backgroundImage,
                    webkitBackgroundClip: style.webkitBackgroundClip,
                    backgroundClip: style.backgroundClip
                };
            }""")
            
            print("Platform text gradient style:", json.dumps(gradient_style, indent=2))
            
            # Check if the gradient contains the expected colors
            gradient_str = json.dumps(gradient_style)
            if "#FF4365" in gradient_str and "#e6a612" in gradient_str and "#f8030c" in gradient_str:
                print("✅ Platform text has the correct gradient colors (red #FF4365 to yellow #e6a612 to red #f8030c)")
            else:
                print("❌ Platform text does not have the expected gradient colors")
        else:
            print("❌ Could not find platform text element")
        
        # Check the hero section background opacity
        hero_style = await page.evaluate("""() => {
            const element = document.querySelector('.hero-section');
            const style = window.getComputedStyle(element);
            return {
                backgroundImage: style.backgroundImage,
                backgroundColor: style.backgroundColor
            };
        }""")
        
        print("Hero section background style:", json.dumps(hero_style, indent=2))
        
        # Check if the background contains rgba with 0.5 opacity
        hero_style_str = json.dumps(hero_style)
        if "rgba(15, 15, 16, 0.5)" in hero_style_str:
            print("✅ Hero background has the correct opacity (0.5)")
        else:
            print("❌ Hero background does not have the expected opacity")
        
        # Check section titles for consistent gradient colors
        section_titles = await page.query_selector_all(".section-title-fixed")
        if section_titles:
            print(f"Found {len(section_titles)} section titles")
            
            # Check the first section title's gradient
            first_title_style = await page.evaluate("""() => {
                const element = document.querySelector('.section-title-fixed');
                const style = window.getComputedStyle(element);
                return {
                    background: style.background,
                    backgroundImage: style.backgroundImage
                };
            }""")
            
            print("Section title gradient style:", json.dumps(first_title_style, indent=2))
            
            # Check if the gradient contains the expected colors
            title_style_str = json.dumps(first_title_style)
            if "#FF4365" in title_style_str and "#e6a612" in title_style_str and "#f8030c" in title_style_str:
                print("✅ Section titles have the correct gradient colors")
            else:
                print("❌ Section titles do not have the expected gradient colors")
        else:
            print("❌ Could not find any section title elements")
        
        # Check if the pulse animation is still working
        platform_text_animation = await page.evaluate("""() => {
            const element = document.querySelector('.platform-gradient-text');
            const style = window.getComputedStyle(element);
            return {
                animation: style.animation
            };
        }""")
        
        print("Platform text animation:", json.dumps(platform_text_animation, indent=2))
        
        if "platform-pulse" in json.dumps(platform_text_animation):
            print("✅ Platform text has the pulse animation")
        else:
            print("❌ Platform text does not have the pulse animation")
        
        # Take a screenshot of the full page to show all section titles
        await page.set_viewport_size({"width": 1920, "height": 4000})
        await page.screenshot(path="full_page.png")
        print("✅ Full page screenshot saved")
        
        # Close the browser
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_ui_changes())