# Browser-Use-Gemini with Pause Feature

This package integrates Google's Gemini model with the browser-use library, adding a critical pause feature that allows users to input sensitive information (like passwords) during browser automation.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/browser-use-gemini-pause.git
cd browser-use-gemini-pause
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

## Configuration

Create a `.env` file in the root directory with your Gemini API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

### Basic Usage

```python
import asyncio
import os
from dotenv import load_dotenv
from browser_use_gemini_pause import GeminiAgent, PauseConditions

# Load environment variables
load_dotenv()

async def main():
    # Create agent with pause capability
    agent = GeminiAgent(
        task="Log into my email account",
        gemini_api_key=os.getenv("GEMINI_API_KEY")
    )
    
    # Add pause conditions
    agent.add_pause_condition(
        PauseConditions.password_field,
        message="Password field detected. Please enter your password:"
    )
    
    # Run the agent
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Usage

You can use the advanced utilities provided in the `utils.py` module for more sophisticated pause conditions:

```python
from utils import AdvancedPauseConditions, PauseManager

# Create a pause manager to track pause events
pause_manager = PauseManager()

# Add advanced pause conditions
agent.add_pause_condition(
    AdvancedPauseConditions.payment_form,
    message="Payment form detected. Please enter your payment details manually:"
)

agent.add_pause_condition(
    AdvancedPauseConditions.captcha,
    message="CAPTCHA detected. Please solve the CAPTCHA manually:"
)
```

### Custom Pause Conditions

You can create custom pause conditions for specific scenarios:

```python
# Define a custom pause condition
async def my_custom_condition(agent_obj):
    url = agent_obj.browser_context.current_url
    page_content = await agent_obj.browser_context.get_page_html()
    
    # Check for specific conditions
    return "specific_text" in page_content or "specific_url_part" in url

# Add the custom condition
agent.add_pause_condition(
    PauseConditions.custom_condition(my_custom_condition),
    message="Custom condition triggered. Please provide input:"
)
```

## Examples

See the `example.py` file for a complete example of how to use the GeminiAgent with pause capability.

## Testing

Run the test script to verify the functionality:

```bash
python test.py
```

This will open a browser, navigate to a demo login page, and pause when a password field is detected.

## Components

- **GeminiAgent**: Main agent class that uses Gemini as the LLM provider and supports pausing
- **PauseConditions**: Predefined conditions that trigger pauses
- **AdvancedPauseConditions**: More sophisticated pause conditions for specific scenarios
- **PauseManager**: Utility for tracking pause events
- **PasswordFieldDetector**: Advanced detector for password fields
- **SensitivePageDetector**: Detector for pages that might contain sensitive information

## License

MIT
