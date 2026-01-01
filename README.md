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
pip install bdd-test-helpers
or
pip install git+https://github.com/kislayPS/bdd-selenium-helper.git

# to uninstall
pip uninstall bdd-test-helpers

# Usage in *_steps.py

from behave_python.helper_func import safe_fill_web_elements
from your_app.models import AccountingVouchers

....
....

@given(u'a business user logged in')
def step_impl(context):
  # save email on context dict for further usage in the same step file
  context.email = 'your.email@gmail.com'

  # clear and send `context.email` in form element id `id_login`
  safe_fill_web_elements(context.browser, 'id_login', context.email)

  # submit button with `id_submit`
  safe_fill_web_elements(context.browser, 'id_submit', click=True)

....
....

@then(u'the user checks year and voucher serial in voucher number')
def impl_step(context):
  # store content of django form html element id "id_entry-voucher_number" in variable name voucher_number
  voucher_number = safe_fill_web_elements(context.browser, 'id_entry-voucher_number')

  # get last accounting voucher from your app in django
  last_voucher = AccountingVouchers.objects.last()

  # store expected voucher serial number
  expected_voucher_number = int(last_voucher.voucher_number.split('/')[-1])+1

  # assert for `expected_voucher_number` in `voucher_number`
  assert expected_voucher_number in voucher_number, f"voucher# {voucher_number} doesn't contain {expected_voucher_number}"





