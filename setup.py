from setuptools import setup, find_packages

setup(
    name="browser-use-gemini-pause",
    version="0.1.0",
    description="Integration of Google's Gemini model with browser-use, adding pause capability for user input",
    author="Manus AI",
    packages=find_packages(),
    install_requires=[
        "browser-use>=0.1.40",
        "google-generativeai>=0.3.0",
        "playwright>=1.40.0",
        "python-dotenv>=1.0.0",
        "asyncio>=3.4.3"
    ],
    python_requires=">=3.11",
)
