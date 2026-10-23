
"""UI tests for the SauceDemo inventory/dashboard module."""

import re

import pytest
from playwright.sync_api import Page, expect


BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"


@pytest.fixture
def inventory_page(page: Page) -> Page:
    """Log in and return a page displaying the inventory."""
    page.goto(BASE_URL)

    page.locator('[data-test="username"]').fill(USERNAME)
    page.locator('[data-test="password"]').fill(PASSWORD)
    page.locator('[data-test="login-button"]').click()

    expect(page).to_have_url(re.compile(r".*/inventory\.html$"))
    expect(page.get_by_text("Products", exact=True)).to_be_visible()

    return page


def test_inventory_page_displays_products(inventory_page: Page) -> None:
    """Verify that product names and prices are visible."""
    products = inventory_page.locator(".inventory_item")

    expect(products.first).to_be_visible()
    expect(products).not_to_have_count(0)

    expect(
        inventory_page.locator(".inventory_item_name").first
    ).to_be_visible()

    expect(
        inventory_page.locator(".inventory_item_price").first
    ).to_be_visible()


def test_inventory_displays_six_products(inventory_page: Page) -> None:
    """Verify the expected number of products in the standard inventory."""
    products = inventory_page.locator(".inventory_item")

    expect(products).to_have_count(6)


def test_inventory_can_be_sorted_by_price_low_to_high(
    inventory_page: Page,
) -> None:
    """Verify that selecting price ascending sorts products correctly."""
    sort_dropdown = inventory_page.locator(
        '[data-test="product-sort-container"]'
    )

    expect(sort_dropdown).to_be_visible()
    sort_dropdown.select_option("lohi")

    prices = inventory_page.locator(".inventory_item_price").all_text_contents()
    numeric_prices = [
        float(price.strip().replace("$", ""))
        for price in prices
    ]

    assert len(numeric_prices) == 6, (
        f"Expected 6 product prices, found {len(numeric_prices)}"
    )
    assert numeric_prices == sorted(numeric_prices), (
        f"Products are not sorted by ascending price: {numeric_prices}"
    )


def test_adding_product_updates_cart_badge(inventory_page: Page) -> None:
    """Verify that adding a product updates the shopping cart count."""
    add_to_cart_button = inventory_page.locator(
        '[data-test="add-to-cart-sauce-labs-backpack"]'
    )

    expect(add_to_cart_button).to_be_visible()
    add_to_cart_button.click()

    cart_badge = inventory_page.locator(
        '[data-test="shopping-cart-badge"]'
    )
    expect(cart_badge).to_have_text("1")

    expect(
        inventory_page.locator(
            '[data-test="remove-sauce-labs-backpack"]'
        )
    ).to_be_visible()


def test_shopping_cart_navigation_opens_cart_page(
    inventory_page: Page,
) -> None:
    """Verify that the shopping cart link opens the cart page."""
    inventory_page.locator(
        '[data-test="shopping-cart-link"]'
    ).click()

    expect(inventory_page).to_have_url(re.compile(r".*/cart\.html$"))
    expect(
        inventory_page.get_by_text("Your Cart", exact=True)
    ).to_be_visible()
