import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException, StaleElementReferenceException

def safe_fill_web_elements(
    browser,
    locator_value: str,
    value: str = None,
    locator_by: By = By.ID,
    timeout: int = 10,
    is_select2: bool = False,
    click: bool = False
):
    """
    Universal helper to safely interact with inputs, selects, select2s, and buttons.

    :param browser: Selenium WebDriver instance
    :param locator_value: str - The ID, CSS selector, XPath, etc.
    :param value: str|None - The text/value to input or select
    :param locator_by: selenium.webdriver.common.by.By - Default By.ID
    :param timeout: int - Wait timeout in seconds
    :param is_select2: bool - Whether the target is a Select2 widget
    :param click: bool - Whether to click the element instead of typing/selecting
    """

    wait = WebDriverWait(browser, timeout)
    element = wait.until(EC.presence_of_element_located((locator_by, locator_value)))

    # Scroll into center view
    browser.execute_script("""
        const el = arguments[0];
        el.scrollIntoView({behavior: 'instant', block: 'center', inline: 'center'});
    """, element)
    ActionChains(browser).move_to_element(element).perform()
    
    tag_name = element.tag_name.lower()

    # Handle clicks
    if click:
        try:
            element.click()
        except ElementNotInteractableException:
            browser.execute_script("arguments[0].click();", element)
        return element

    if value is None:
        text_value = ""
        if tag_name in ("input", "textarea"):
            text_value = element.get_attribute("value") or ""
            # Handle readonly or hidden inputs
            if not text_value.strip():
                text_value = browser.execute_script("return arguments[0].textContent;", element) or ""
        elif tag_name == "select":
            try:
                select = Select(element)
                selected_option = select.first_selected_option
                text_value = selected_option.text.strip()
            except Exception:
                text_value = element.get_attribute("value") or ""
        elif is_select2:
            try:
                selected_el = browser.find_element(By.CSS_SELECTOR, ".select2-selection__rendered")
                text_value = selected_el.text.strip()
            except NoSuchElementException:
                text_value = ""
        else:
            # For generic divs/spans
            text_value = element.text.strip() or element.get_attribute("textContent").strip()

        return text_value
    # Handle Select2 widgets
    if is_select2:
        try:
            # Click to open dropdown
            element.click()
            time.sleep(1.5)
            search_box = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "select2-search__field"))
            )
            search_box.send_keys(value)
            search_box.send_keys(Keys.ENTER)  # Press ENTER
            time.sleep(1.5)

        except TimeoutException:
            raise AssertionError(f"Select2 element not interactable for locator {locator_value}")
        return element

    # Handle native <select> dropdowns
    tag_name = element.tag_name.lower()
    if tag_name == "select":
        select = Select(element)
        try:
            select.select_by_visible_text(value)
        except NoSuchElementException:
            # Try selecting by value if visible text not found
            select.select_by_value(value)
        return element

    # Handle <input>, <textarea>
    try:
        element.clear()
        if value is not None:
            element.send_keys(value)
    except (ElementNotInteractableException, MoveTargetOutOfBoundsException):
        time.sleep(0.3)
        browser.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center', inline: 'center'});", element)
        element.clear()
        if value is not None:
            element.send_keys(value)

    # Verify final value if applicable
    if value is not None and tag_name in ("input", "textarea"):
        final_value = element.get_attribute("value")
        assert str(value) in final_value, \
            f"Expected '{value}' in #{locator_value}, but got '{final_value}'"

    return element


def set_value_and_trigger(browser, element, value):
    browser.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
    """, element, str(value))


def check_webpage_errors_present(driver):
    """
    Checks for error in the webpage when form is processed
    """
    try:
        error_elements = driver.find_elements(By.CLASS_NAME, 'errorlist')

        visible_errors = [
            e.text for e in error_elements
            if e.is_displayed() and e.text.strip()
        ]

        if visible_errors:
            raise AssertionError(
                f'Validation errors found: {visible_errors}'
            )

        return True

    except StaleElementReferenceException:
        return False

def get_table_row_by_table_text(
            driver,
            search_text: str,
            expected_count: int = 1,
            timeout: int = 10,
        ):
    """
    Find table row(s) containing `search_text` and return their row text.

    Returns:
        list[str]  # row texts
    """    
    xpath = (
        f"//table//*[substring(normalize-space(text()), "
        f"string-length(normalize-space(text())) - string-length('{search_text}') + 1) "
        f"= '{search_text}']"
    )

    cells = WebDriverWait(driver, timeout).until(
        lambda d: d.find_elements(By.XPATH, xpath)
    )

    assert len(cells) == expected_count, (
        f"Expected {expected_count} row(s) containing '{search_text}', "
        f"found {len(cells)}"
    )

    return [cell.find_element(By.XPATH, "ancestor::tr") for cell in cells]
