# bdd-selenium-helper
Behave Helper functions that standardize and simplify Behavior-Driven Development (BDD) by encapsulating commonly repeated steps into reusable functions. These helpers allow teams to write cleaner, more readable BDD scenarios while ensuring consistency across Django test suites.

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
from your_app.models imports AccountingVouchers

....
....
....

@then(u'the user checks year and voucher serial in voucher number')
def impl_step(context):
  voucher_number = safe_fill_web_elements(context.browser, 'id_entry-voucher_number')
  last_voucher = AccountingVouchers.objects.last()
  should_be_next_voucher_number = int(last_voucher.voucher_number.split('/')[-1])+1
  assert should_be_next_voucher_number in voucher_number, f"voucher# {voucher_number} doesn't contain {should_be_next_voucher_number}"


# to uninstall
pip uninstall bdd-test-helpers
