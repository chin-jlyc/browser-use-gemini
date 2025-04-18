"""
Browser-Use-Gemini with Pause Feature

This module integrates Google's Gemini model with the browser-use library,
adding a pause feature that allows users to input sensitive information
during browser automation.
"""

import asyncio
import os
from typing import Any, Callable, Dict, List, Optional, Union

# Import browser-use components
from browser_use import Agent
from browser_use.agent.hooks import HookManager

# Import Gemini components
import google.generativeai as genai

class GeminiLLMWrapper:
    """
    Wrapper for Gemini model to make it compatible with browser-use's expected LLM interface.
    """
    
    def __init__(self, gemini_model):
        """
        Initialize the wrapper with a Gemini model.
        
        Args:
            gemini_model: The Gemini model instance
        """
        self.model = gemini_model
    
    async def __call__(self, prompt: str, **kwargs) -> Dict[str, str]:
        """
        Call the Gemini model with the prompt.
        
        Args:
            prompt: The prompt to send to the model
            **kwargs: Additional arguments to pass to the model
            
        Returns:
            Dict containing the model's response
        """
        # Call Gemini model with the prompt
        response = await self.model.generate_content_async(prompt)
        
        # Format response to match browser-use expectations
        return {"content": response.text}


class UserInputHandler:
    """
    Handles getting input from the user during pauses.
    """
    
    def __init__(self, input_method: str = "console"):
        """
        Initialize the input handler.
        
        Args:
            input_method: Method to use for getting user input ("console" or "web")
        """
        self.input_method = input_method
    
    async def get_input(self, prompt: str) -> str:
        """
        Get input from the user.
        
        Args:
            prompt: The prompt to display to the user
            
        Returns:
            The user's input
        """
        if self.input_method == "console":
            # For console input, we need to run in a thread to not block the event loop
            return await asyncio.to_thread(input, prompt)
        elif self.input_method == "web":
            # Web-based input would be implemented here
            raise NotImplementedError("Web-based input not yet implemented")
        else:
            raise ValueError(f"Unknown input method: {self.input_method}")


class PauseHook:
    """
    Hook system for pausing execution at specific points.
    """
    
    def __init__(self, agent, input_handler: Optional[UserInputHandler] = None):
        """
        Initialize the pause hook.
        
        Args:
            agent: The agent instance
            input_handler: Handler for user input during pauses
        """
        self.agent = agent
        self.paused = False
        self.pause_conditions = []
        self.user_input = None
        self.input_handler = input_handler or UserInputHandler()
    
    def register_hooks(self):
        """Register hooks with the agent."""
        # Register before_step hook to check for pause conditions
        self.agent.hooks.register_hook("before_step", self.check_pause_condition)
    
    async def check_pause_condition(self, agent_obj):
        """
        Check if any pause condition is met.
        
        Args:
            agent_obj: The agent instance
        """
        # Check if any pause condition is met
        for condition, message in self.pause_conditions:
            if await condition(agent_obj):
                self.paused = True
                # Notify user and wait for input
                await self.handle_pause(agent_obj, message)
                break
    
    async def handle_pause(self, agent_obj, message: str):
        """
        Handle a pause in execution.
        
        Args:
            agent_obj: The agent instance
            message: Message to display to the user
        """
        print("\n" + "="*50)
        print(f"EXECUTION PAUSED: {message}")
        print("="*50)
        
        # Get input from user
        self.user_input = await self.input_handler.get_input("Enter your input: ")
        
        print("Continuing execution...\n")
        self.paused = False
    
    def add_pause_condition(self, condition: Callable, message: str = "User input required"):
        """
        Add a new condition that will trigger a pause.
        
        Args:
            condition: Function that returns True when execution should pause
            message: Message to display to the user when paused
        """
        self.pause_conditions.append((condition, message))


class PauseConditions:
    """
    Predefined pause conditions.
    """
    
    @staticmethod
    async def password_field(agent_obj) -> bool:
        """
        Pause when a password field is detected.
        
        Args:
            agent_obj: The agent instance
            
        Returns:
            True if a password field is detected, False otherwise
        """
        # Get current page content
        page_content = await agent_obj.browser_context.get_page_html()
        
        # Check if there's a password field
        return 'type="password"' in page_content
    
    @staticmethod
    async def login_page(agent_obj) -> bool:
        """
        Pause when a login page is detected.
        
        Args:
            agent_obj: The agent instance
            
        Returns:
            True if a login page is detected, False otherwise
        """
        # Get current URL
        url = agent_obj.browser_context.current_url
        
        # Check if URL contains login indicators
        return any(term in url.lower() for term in ['login', 'signin', 'auth'])
    
    @staticmethod
    def custom_condition(check_function: Callable) -> Callable:
        """
        Create a custom pause condition.
        
        Args:
            check_function: Function that returns True when execution should pause
            
        Returns:
            A pause condition function
        """
        async def condition(agent_obj):
            return await check_function(agent_obj)
        
        return condition


class GeminiAgent(Agent):
    """
    Agent that uses Gemini as the LLM provider and supports pausing.
    """
    
    def __init__(
        self, 
        task: str, 
        gemini_api_key: str, 
        model_name: str = "gemini-pro",
        input_method: str = "console",
        **kwargs
    ):
        """
        Initialize the Gemini agent.
        
        Args:
            task: The task to perform
            gemini_api_key: API key for Gemini
            model_name: Name of the Gemini model to use
            input_method: Method to use for getting user input
            **kwargs: Additional arguments to pass to the Agent constructor
        """
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        
        # Create Gemini model
        gemini_model = genai.GenerativeModel(model_name)
        
        # Create LLM wrapper
        llm = GeminiLLMWrapper(gemini_model)
        
        # Initialize the base Agent with Gemini LLM
        super().__init__(task=task, llm=llm, **kwargs)
        
        # Set up pause functionality
        self.input_handler = UserInputHandler(input_method=input_method)
        self.pause_hook = PauseHook(self, self.input_handler)
        self.pause_hook.register_hooks()
    
    def add_pause_condition(self, condition: Callable, message: str = "User input required"):
        """
        Add a condition that will trigger a pause.
        
        Args:
            condition: Function that returns True when execution should pause
            message: Message to display to the user when paused
        """
        self.pause_hook.add_pause_condition(condition, message)
