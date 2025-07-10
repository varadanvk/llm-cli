# Changelog

All notable changes to this project will be documented in this file.

## [0.0.7] - 2025-01-10

### Added
- Full OpenRouter support with multiple model options
- Custom model selection for OpenRouter (select "custom" then enter any model name)
- Available OpenRouter models:
  - google/gemini-2.5-pro
  - x-ai/grok-3
  - x-ai/grok-4
  - custom (allows any OpenRouter model)
- Load API keys from .env file during setup
- Enhanced setup process with choice between manual entry or .env file loading
- Summary display of configured providers after setup

### Changed
- Setup now offers two options: manual API key entry or loading from .env file
- Improved error handling for missing .env files

### Fixed
- Minor syntax fixes in model configuration

## [0.0.6] - Previous release
- Previous features and fixes