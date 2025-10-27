from setuptools import setup

setup(
    name="cli-chat",
    version="1.0.0",
    py_modules=["chat"],  
    install_requires=[
        "asyncio",         
        "websockets>=12.0",
        "prompt_toolkit>=3.0.0",
        "rich>=13.0.0",
        "fastapi>=0.110.0",
        "python-dotenv>=1.0.0",
        "uvicorn>=0.23.0",  
    ],
    entry_points={
        "console_scripts": [
            "chat=chat:main", 
        ],
    },
    author="Your Name",
    description="A CLI and WebSocket-based chat application using FastAPI and prompt_toolkit",
    python_requires=">=3.8",
)
