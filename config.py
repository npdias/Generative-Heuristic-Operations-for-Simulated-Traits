# Purpose: Centralizes application configuration and settings.
# Responsibilities:
# Stores configurations such as file paths, API keys, default parameters, or logging preferences.
# Facilitates environment-specific configurations using .env files or environment variables.
# Provides a single access point for configurations throughout the application to avoid hardcoding settings in multiple places.
# May include utility functions to parse or validate configurations.

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')