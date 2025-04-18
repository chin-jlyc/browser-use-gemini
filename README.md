# Browser-Use-Gemini with Pause Feature

This tool integrates Google's Gemini model with the browser-use library, adding a critical pause feature that allows users to input sensitive information (like passwords) during browser automation.

## Features

- Uses Gemini as the LLM provider for browser automation
- Implements a pause mechanism to allow user input at specific points
- Continues execution after receiving user input
- Provides a simple API for defining pause points in your automation tasks

## How It Works

The tool builds on the browser-use library's hook system to implement a pause mechanism. When the automation reaches a point where user input is needed (such as a password field), it:

1. Pauses execution
2. Notifies the user that input is required
3. Waits for the user to provide the necessary information
4. Continues execution with the provided input

## Requirements

- Python 3.11+
- browser-use library
- Google API key for Gemini access
- Playwright (for browser automation)
