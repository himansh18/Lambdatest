
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"


@pytest.fixture(autouse=True)
def open_login_page(page: Page):
    page.goto(BASE_URL)


def test_empty_login_shows_username_required(page: Page):
    page.get_by_role("button", name="Login").click()

    expect(page.locator('[data-test="error"]')).to_have_text(
        "Epic sadface: Username is required"
    )


def test_empty_password_shows_password_required(page: Page):
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_role("button", name="Login").click()

    expect(page.locator('[data-test="error"]')).to_have_text(
        "Epic sadface: Password is required"
    )


def test_wrong_password_shows_error(page: Page):
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("wrong_pass")
    page.get_by_role("button", name="Login").click()

    expect(page.locator('[data-test="error"]')).to_have_text(
        "Epic sadface: Username and password do not match any user in this service"
    )


def test_locked_out_user_cannot_login(page: Page):
    page.get_by_placeholder("Username").fill("locked_out_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    expect(page.locator('[data-test="error"]')).to_have_text(
        "Epic sadface: Sorry, this user has been locked out."
    )


def test_standard_user_can_login(page: Page):
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator(".inventory_list")).to_be_visible()
