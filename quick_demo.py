"""
Quick demo script for Browser-Use-Gemini with Pause Feature.

This script demonstrates how to use the GeminiAgent with a visible browser
and manual control for login scenarios.
"""

import asyncio
import os
from dotenv import load_dotenv

from browser_use_gemini_pause import GeminiAgent, PauseConditions
from utils import AdvancedPauseConditions

# Load environment variables from .env file
load_dotenv()

async def main():
    # Get Gemini API key from environment variable
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("GEMINI_API_KEY environment variable not set.")
        print("For this demo, we'll use a placeholder that won't make actual API calls.")
        gemini_api_key = "PLACEHOLDER_API_KEY"  # This won't work for actual API calls
    
    print("Starting Browser-Use-Gemini with Pause Feature demo...")
    print("A visible browser window will open and you'll be able to take control when needed.")
    
    # Create agent with pause capability and visible browser
    agent = GeminiAgent(
        task="Navigate to a website that requires login",
        gemini_api_key=gemini_api_key,
        headless=False  # Make sure the browser is visible
    )
    
    # Add pause conditions for login scenarios
    agent.add_pause_condition(
        PauseConditions.password_field,
        message="Password field detected. Please enter your credentials in the browser window."
    )
    
    agent.add_pause_condition(
        PauseConditions.login_page,
        message="Login page detected. You can now take control of the browser."
    )
    
    agent.add_pause_condition(
        AdvancedPauseConditions.captcha,
        message="CAPTCHA detected. Please solve it manually in the browser window."
    )
    
    try:
        # Initialize the browser
        await agent.initialize()
        
        # Navigate to a demo site that has a login form
        print("\nNavigating to a demo site with login form...")
        await agent.browser_context.goto("https://demo.applitools.com/")
        
        # Wait for the page to load
        await asyncio.sleep(2)
        
        # Click the login button to go to the login form
        print("Clicking the Sign in button...")
        await agent.browser_context.click_by_text("Sign in")
        
        # This should trigger the password field pause condition
        # The execution will pause and you can take control of the browser
        print("\nYou should now be able to interact with the login form.")
        print("The automation is paused until you provide input in the console.")
        
        # Wait for user to finish interacting with the browser
        input("\nPress Enter when you're done interacting with the browser...")
        
        print("Demo completed successfully!")
        
    except Exception as e:
        print(f"Error during demo: {e}")
    finally:
        # Ask before closing the browser
        input("\nPress Enter to close the browser and end the demo...")
        # Clean up
        await agent.browser_context.close()
        print("Browser closed. Demo ended.")

if __name__ == "__main__":
    asyncio.run(main())
