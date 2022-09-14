from setuptools import setup, find_namespace_packages

setup(name="helper-bot-team-1",
      version="1.0.0",
      description="Personal assistant bot that manages contacts, notes and can organize user's folders.",
      url="https://github.com/PavelDushinskiy/GoIT-Core-Project",
      author="Yanina Lubenska, Eugene Vyshnytsky, Pavel Dushinskiy",
      packages=find_namespace_packages(),
      entry_points={"console_scripts": ["helper-bot=helper-bot-team-1.main:run_app"]}
      )
