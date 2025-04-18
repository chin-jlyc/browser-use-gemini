"""
Example usage of the Browser-Use-Gemini with Pause Feature.

This script demonstrates how to use the GeminiAgent with pause capability
to automate browser tasks while allowing user input at specific points.
"""

import asyncio
import os
from dotenv import load_dotenv

from browser_use_gemini_pause import GeminiAgent, PauseConditions

# Load environment variables from .env file
load_dotenv()

async def main():
    # Get Gemini API key from environment variable
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    # Create agent with pause capability
    agent = GeminiAgent(
        task="Log into a website and perform some actions",
        gemini_api_key=gemini_api_key
    )
    
    # Add predefined pause conditions
    agent.add_pause_condition(
        PauseConditions.password_field,
        message="Password field detected. Please enter your password:"
    )
    
    agent.add_pause_condition(
        PauseConditions.login_page,
        message="Login page detected. You may need to enter credentials."
    )
    
    # Add a custom pause condition (example: pause on payment pages)
    async def payment_page_condition(agent_obj):
        url = agent_obj.browser_context.current_url
        page_content = await agent_obj.browser_context.get_page_html()
        return (
            any(term in url.lower() for term in ['payment', 'checkout', 'billing']) or
            any(term in page_content.lower() for term in ['credit card', 'payment method', 'cvv'])
        )
    
    agent.add_pause_condition(
        PauseConditions.custom_condition(payment_page_condition),
        message="Payment page detected. Please enter your payment details manually."
    )
    
    # Run the agent
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
