"""
Utility functions for Browser-Use-Gemini with Pause Feature.

This module provides additional utility functions to enhance the functionality
of the GeminiAgent with pause capability.
"""

import asyncio
import os
import json
from typing import Any, Dict, List, Optional, Union

class PauseManager:
    """
    Manages pause points and user interactions during browser automation.
    """
    
    def __init__(self):
        """Initialize the pause manager."""
        self.pause_history = []
        self.input_history = {}
    
    def record_pause(self, url: str, reason: str, user_input: str):
        """
        Record a pause event.
        
        Args:
            url: The URL where the pause occurred
            reason: The reason for the pause
            user_input: The input provided by the user
        """
        # Don't store actual passwords or sensitive data, just record that input was provided
        sanitized_input = "[INPUT PROVIDED]" if user_input else "[NO INPUT]"
        
        pause_event = {
            "url": url,
            "reason": reason,
            "input_provided": bool(user_input),
            "timestamp": asyncio.get_event_loop().time()
        }
        
        self.pause_history.append(pause_event)
    
    def get_pause_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of pause events.
        
        Returns:
            List of pause events
        """
        return self.pause_history
    
    def save_history(self, filename: str):
        """
        Save the pause history to a file.
        
        Args:
            filename: The name of the file to save to
        """
        with open(filename, 'w') as f:
            json.dump(self.pause_history, f, indent=2)


class PasswordFieldDetector:
    """
    Advanced detector for password fields with various detection methods.
    """
    
    @staticmethod
    async def detect_password_field(agent_obj) -> bool:
        """
        Detect password fields using multiple methods.
        
        Args:
            agent_obj: The agent instance
            
        Returns:
            True if a password field is detected, False otherwise
        """
        # Get current page content
        page_content = await agent_obj.browser_context.get_page_html()
        
        # Method 1: Check for password input type
        if 'type="password"' in page_content or "type='password'" in page_content:
            return True
        
        # Method 2: Check for common password field IDs and names
        password_indicators = [
            'id="password"', "id='password'", 'name="password"', "name='password'",
            'id="pwd"', "id='pwd'", 'name="pwd"', "name='pwd'",
            'id="pass"', "id='pass'", 'name="pass"', "name='pass'"
        ]
        
        for indicator in password_indicators:
            if indicator in page_content:
                return True
        
        # Method 3: Check for password-related labels
        password_labels = [
            '>Password<', '>password<', '>Pass<', '>pass<',
            '>Enter password<', '>Enter your password<'
        ]
        
        for label in password_labels:
            if label in page_content:
                return True
        
        return False


class SensitivePageDetector:
    """
    Detects pages that might contain sensitive information or require user input.
    """
    
    @staticmethod
    async def detect_sensitive_page(agent_obj) -> Dict[str, bool]:
        """
        Detect various types of sensitive pages.
        
        Args:
            agent_obj: The agent instance
            
        Returns:
            Dictionary with detection results for different page types
        """
        url = agent_obj.browser_context.current_url
        page_content = await agent_obj.browser_context.get_page_html()
        
        results = {
            "login_page": False,
            "payment_page": False,
            "personal_info_page": False,
            "two_factor_auth_page": False
        }
        
        # Login page detection
        login_indicators = ['login', 'signin', 'sign-in', 'log-in', 'auth']
        if any(indicator in url.lower() for indicator in login_indicators):
            results["login_page"] = True
        
        # Payment page detection
        payment_indicators = [
            'payment', 'checkout', 'billing', 'credit card', 'creditcard',
            'card number', 'cvv', 'cvc', 'expiration date'
        ]
        if any(indicator in url.lower() or indicator in page_content.lower() 
               for indicator in payment_indicators):
            results["payment_page"] = True
        
        # Personal information page detection
        personal_info_indicators = [
            'address', 'personal', 'profile', 'account details',
            'social security', 'ssn', 'date of birth', 'birthdate'
        ]
        if any(indicator in url.lower() or indicator in page_content.lower() 
               for indicator in personal_info_indicators):
            results["personal_info_page"] = True
        
        # Two-factor authentication detection
        two_factor_indicators = [
            'two-factor', 'two factor', '2fa', 'verification code',
            'security code', 'authenticate', 'verification'
        ]
        if any(indicator in url.lower() or indicator in page_content.lower() 
               for indicator in two_factor_indicators):
            results["two_factor_auth_page"] = True
        
        return results


# Additional pause conditions that can be used with GeminiAgent
class AdvancedPauseConditions:
    """
    Advanced pause conditions for specific scenarios.
    """
    
    @staticmethod
    async def payment_form(agent_obj) -> bool:
        """
        Pause when a payment form is detected.
        
        Args:
            agent_obj: The agent instance
            
        Returns:
            True if a payment form is detected, False otherwise
        """
        page_content = await agent_obj.browser_context.get_page_html()
        payment_indicators = [
            'credit card', 'debit card', 'card number', 'cvv', 'cvc',
            'expiration date', 'expiry date', 'billing address'
        ]
        return any(indicator in page_content.lower() for indicator in payment_indicators)
    
    @staticmethod
    async def two_factor_auth(agent_obj) -> bool:
        """
        Pause when a two-factor authentication page is detected.
        
        Args:
            agent_obj: The agent instance
            
        Returns:
            True if a 2FA page is detected, False otherwise
        """
        page_content = await agent_obj.browser_context.get_page_html()
        url = agent_obj.browser_context.current_url
        
        two_factor_indicators = [
            'two-factor', 'two factor', '2fa', 'verification code',
            'security code', 'authenticate', 'verification'
        ]
        
        return any(indicator in url.lower() or indicator in page_content.lower() 
                  for indicator in two_factor_indicators)
    
    @staticmethod
    async def captcha(agent_obj) -> bool:
        """
        Pause when a CAPTCHA is detected.
        
        Args:
            agent_obj: The agent instance
            
        Returns:
            True if a CAPTCHA is detected, False otherwise
        """
        page_content = await agent_obj.browser_context.get_page_html()
        captcha_indicators = [
            'captcha', 'recaptcha', 'i\'m not a robot', 'im not a robot',
            'verify you\'re human', 'verify youre human'
        ]
        return any(indicator in page_content.lower() for indicator in captcha_indicators)
    
    @staticmethod
    async def personal_information_form(agent_obj) -> bool:
        """
        Pause when a form requesting personal information is detected.
        
        Args:
            agent_obj: The agent instance
            
        Returns:
            True if a personal information form is detected, False otherwise
        """
        page_content = await agent_obj.browser_context.get_page_html()
        personal_info_indicators = [
            'social security', 'ssn', 'date of birth', 'birthdate',
            'passport', 'driver\'s license', 'drivers license',
            'identity verification', 'government id'
        ]
        return any(indicator in page_content.lower() for indicator in personal_info_indicators)
