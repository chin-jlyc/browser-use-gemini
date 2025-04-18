"""
Test script for Browser-Use-Gemini with Pause Feature.

This script tests the functionality of the GeminiAgent with pause capability
by automating a simple task that requires user input at specific points.
"""

import asyncio
import os
from dotenv import load_dotenv

from browser_use_gemini_pause import GeminiAgent, PauseConditions
from utils import AdvancedPauseConditions, PauseManager

# Load environment variables from .env file
load_dotenv()

async def test_login_with_pause():
    """Test the pause feature with a login scenario."""
    # Get Gemini API key from environment variable
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("GEMINI_API_KEY environment variable not set. Using a placeholder for testing.")
        gemini_api_key = "PLACEHOLDER_API_KEY"  # This won't work for actual API calls
    
    # Create a pause manager to track pause events
    pause_manager = PauseManager()
    
    # Create agent with pause capability
    agent = GeminiAgent(
        task="Go to a demo login page and pause when credentials are needed",
        gemini_api_key=gemini_api_key,
        headless=False  # Show the browser for testing
    )
    
    # Add pause conditions
    agent.add_pause_condition(
        PauseConditions.password_field,
        message="Password field detected. Please enter your password:"
    )
    
    agent.add_pause_condition(
        AdvancedPauseConditions.captcha,
        message="CAPTCHA detected. Please solve the CAPTCHA manually:"
    )
    
    # Define a custom pause condition for demonstration
    async def demo_pause_condition(agent_obj):
        # This is just for demonstration - in a real scenario, 
        # you would check for specific conditions
        print("Checking if we should pause...")
        return False
    
    agent.add_pause_condition(
        PauseConditions.custom_condition(demo_pause_condition),
        message="Custom pause condition triggered."
    )
    
    try:
        # Run the agent with a simple task that will trigger the pause
        # For testing, we'll use a simple demo login page
        print("Starting test with pause capability...")
        print("The browser will open and navigate to a login page.")
        print("When a password field is detected, execution will pause.")
        print("You'll be prompted to enter information in the console.")
        print("After you provide input, execution will continue.")
        
        # In a real scenario, you would use agent.run() with your task
        # For testing, we'll simulate the process
        
        # Initialize the browser
        await agent.initialize()
        
        # Navigate to a demo login page
        await agent.browser_context.goto("https://demo.applitools.com/")
        
        # Wait for the page to load
        await asyncio.sleep(2)
        
        # Click the login button to go to the login form
        await agent.browser_context.click_by_text("Sign in")
        
        # This should trigger the password field pause condition
        # The execution will pause and wait for user input
        
        print("\nTest completed. Check if the pause was triggered correctly.")
        
    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        # Clean up
        await agent.browser_context.close()
        print("Browser closed.")

if __name__ == "__main__":
    asyncio.run(test_login_with_pause())
