from setuptools import setup


setup(name="cli_assistant_bot",
      version="1.0.0",
      description="Personal assistant bot that manages contacts, notes and can organize user's folders.",
      url="https://github.com/PavelDushinskiy/GoIT-Core-Project",
      author="Yanina Lubenska, Eugene Vyshnytsky, Pavel Dushinskiy",
      packages=["assistant-bot"],
      entry_points={"console_scripts": ["assistant-bot = assistant-bot.main:run_app"]}
      )