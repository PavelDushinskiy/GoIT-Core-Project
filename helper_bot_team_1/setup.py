from setuptools import setup, find_namespace_packages

setup(name="helper-bot-team-1",
      version="1.0.0",
      description="Personal assistant bot that manages contacts, notes and can organize user's folders.",
      url="https://github.com/PavelDushinskiy/GoIT-Core-Project",
      author="Yanina Lubenska, Eugene Vyshnytsky, Pavel Dushinskiy",
      packages=find_namespace_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "Operating System :: Windows",
      ],
      entry_points={'console_scripts': ['helper_bot=helper_bot_team_1.main:run_app']}
      )