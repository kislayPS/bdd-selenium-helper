# bdd-selenium-helper
Helper functions that standardize and simplify Behavior-Driven Development (BDD) by encapsulating commonly repeated steps into reusable functions. These helpers allow teams to write cleaner, more readable BDD scenarios while ensuring consistency across Django test suites.

# BDD Test Helpers for Django

Reusable helper functions to standardize and simplify
Behavior-Driven Development (BDD) in Python and Django projects.

## Why this exists
- Reduce duplicated test setup
- Improve readability of test scenarios
- Enforce consistent test behavior across teams

## Installation
```bash
pip install git+https://github.com/kislayPS/bdd-selenium-helper.git


# Usage in *_steps.py

from behave_python.helper_func import safe_fill_web_elements
