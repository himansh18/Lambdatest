
Feature: Widget loading - product cards on /inventory.html

  @id-WL-01 @P1 @positive @automatable
  Scenario: Six product cards load after login
    Given the user is on https://www.saucedemo.com
    When the user logs in as "standard_user" with password "secret_sauce"
    Then the URL path is "/inventory.html"
    And exactly 6 product cards are displayed

  @id-WL-02 @P1 @positive @automatable
  Scenario: Every product card shows name, description, price, image and button
    Given the user is logged in as "standard_user" on "/inventory.html"
    When the page has finished loading
    Then each of the 6 product cards contains a non-empty name
    And each of the 6 product cards contains a non-empty description
    And each of the 6 product cards contains a price starting with "$"
    And each of the 6 product cards contains an "Add to cart" button

  @id-WL-03 @P2 @positive @automatable
  Scenario: All product images load successfully
    Given the user is logged in as "standard_user" on "/inventory.html"
    When the page has finished loading
    Then all 6 product card images have a naturalWidth greater than 0

  @id-WL-04 @P2 @positive @automatable
  Scenario: Product cards reload after a page refresh
    Given the user is logged in as "standard_user" on "/inventory.html"
    When the user refreshes the browser page
    Then the URL path is "/inventory.html"
    And exactly 6 product cards are displayed

  @id-WL-05 @P3 @negative @automatable
  Scenario: Cart badge is not rendered when no item has been added
    Given the user is logged in as "standard_user" on "/inventory.html"
    When the page has finished loading
    Then the cart badge element is not present in the header


Feature: Data accuracy - product names and prices

  @id-DA-01 @P1 @positive @automatable
  Scenario: Backpack card displays the exact name and price
    Given the user is logged in as "standard_user" on "/inventory.html"
    When the user reads the card named "Sauce Labs Backpack"
    Then the card price is "$29.99"

  @id-DA-02 @P1 @positive @automatable
  Scenario: All six products display the expected prices
    Given the user is logged in as "standard_user" on "/inventory.html"
    When the user reads the name and price of all 6 cards
    Then "Sauce Labs Bike Light" is priced "$9.99", "Sauce Labs Bolt T-Shirt" "$15.99", "Sauce Labs Fleece Jacket" "$49.99", "Sauce Labs Onesie" "$7.99" and "Test.allTheThings() T-Shirt (Red)" "$15.99"

  @id-DA-03 @P1 @positive @automatable
  Scenario: Cart badge equals the number of items added
    Given the user is logged in as "standard_user" on "/inventory.html"
    When the user clicks "Add to cart" on "Sauce Labs Backpack"
    And the user clicks "Add to cart" on "Sauce Labs Onesie"
    Then the cart badge text is "2"

  @id-DA-04 @P2 @positive @automatable
  Scenario: Price on the inventory card matches the price in the cart
    Given the user is logged in as "standard_user" on "/inventory.html"
    And the user reads the price of "Sauce Labs Fleece Jacket" from its card
    When the user clicks "Add to cart" on "Sauce Labs Fleece Jacket"
    And the user opens the cart page
    Then the cart item price equals the price read from the inventory card

  @id-DA-05 @P2 @negative @automatable
  Scenario: Cart badge disappears after the only added item is removed
    Given the user is logged in as "standard_user" on "/inventory.html"
    And the user clicks "Add to cart" on "Sauce Labs Bike Light"
    When the user clicks "Remove" on "Sauce Labs Bike Light"
    Then the cart badge element is not present in the header

  @id-DA-06 @P3 @negative @automatable
  Scenario: Reset App State clears the cart badge
    Given the user is logged in as "standard_user" on "/inventory.html"
    And the user clicks "Add to cart" on "Sauce Labs Backpack"
    When the user opens the burger menu and clicks "Reset App State"
    Then the cart badge element is not present in the header


Feature: Filter and sort behavior - product sort dropdown

  @id-FS-01 @P1 @positive @automatable
  Scenario: Default sort option is Name (A to Z)
    Given the user is logged in as "standard_user" on "/inventory.html"
    When the page has finished loading
    Then the selected sort option is "Name (A to Z)"

  @id-FS-02 @P1 @positive @automatable
  Scenario: Name (A to Z) lists products alphabetically
    Given the user is logged in as "standard_user" on "/inventory.html"
    When the user selects "Name (A to Z)" from the sort dropdown
    Then the product names in order are "Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie", "Test.allTheThings() T-Shirt (Red)"

  @id-FS-03 @P1 @positive @automatable
  Scenario: Name (Z to A) lists products in reverse alphabetical order
    Given the user is logged in as "standard_user" on "/inventory.html"
    When the user selects "Name (Z to A)" from the sort dropdown
    Then the product names in order are "Test.allTheThings() T-Shirt (Red)", "Sauce Labs Onesie", "Sauce Labs Fleece Jacket", "Sauce Labs Bolt T-Shirt", "Sauce Labs Bike Light", "Sauce Labs Backpack"

  @id-FS-04 @P1 @positive @automatable
  Scenario: Price (low to high) puts the cheapest product first and the dearest last
    Given the user is logged in as "standard_user" on "/inventory.html"
    When the user selects "Price (low to high)" from the sort dropdown
    Then the first card is "Sauce Labs Onesie" at "$7.99"
    And the last card is "Sauce Labs Fleece Jacket" at "$49.99"

  @id-FS-05 @P1 @positive @automatable
  Scenario: Price (high to low) puts the dearest product first and the cheapest last
    Given the user is logged in as "standard_user" on "/inventory.html"
    When the user selects "Price (high to low)" from the sort dropdown
    Then the first card is "Sauce Labs Fleece Jacket" at "$49.99"
    And the last card is "Sauce Labs Onesie" at "$7.99"

  @id-FS-06 @P2 @negative @automatable
  Scenario: Sorting does not change the cart badge count
    Given the user is logged in as "standard_user" on "/inventory.html"
    And the user clicks "Add to cart" on "Sauce Labs Backpack"
    When the user selects "Price (high to low)" from the sort dropdown
    Then the cart badge text is "1"


Feature: Responsive layout - viewport behavior of /inventory.html

  @id-RL-01 @P1 @positive @automatable
  Scenario: Desktop 1920x1080 shows all cards and header controls
    Given the browser viewport is 1920x1080
    When the user logs in as "standard_user" with password "secret_sauce"
    Then exactly 6 product cards are displayed
    And the sort dropdown, cart icon and burger menu button are visible

  @id-RL-02 @P1 @positive @automatable
  Scenario: Tablet 768x1024 shows all cards without horizontal scrolling
    Given the browser viewport is 768x1024
    When the user logs in as "standard_user" with password "secret_sauce"
    Then exactly 6 product cards are displayed
    And the page scrollWidth is less than or equal to the viewport width of 768

  @id-RL-03 @P1 @positive @automatable
  Scenario: Mobile 375x667 shows all cards without horizontal scrolling
    Given the browser viewport is 375x667
    When the user logs in as "standard_user" with password "secret_sauce"
    Then exactly 6 product cards are displayed
    And the page scrollWidth is less than or equal to the viewport width of 375

  @id-RL-04 @P2 @positive @automatable
  Scenario: Burger menu opens and lists four items at 375x667
    Given the browser viewport is 375x667
    And the user is logged in as "standard_user" on "/inventory.html"
    When the user clicks the burger menu button
    Then the menu lists "All Items", "About", "Logout" and "Reset App State"

  @id-RL-05 @P2 @boundary @automatable
  Scenario: Cart badge remains visible at the smallest tested width of 320x568
    Given the browser viewport is 320x568
    And the user is logged in as "standard_user" on "/inventory.html"
    When the user clicks "Add to cart" on "Sauce Labs Backpack"
    Then the cart badge text is "1"

  @id-RL-06 @P3 @positive @design-only
  Scenario: Layout looks visually correct when the viewport is resized from 1920x1080 to 375x667
    Given the user is logged in as "standard_user" on "/inventory.html" at 1920x1080
    When the tester resizes the browser window to 375x667
    Then no product card text or image overlaps another card in a visual review


Feature: Permission-based visibility - authentication and user access (no roles or admin views exist)

  @id-PV-01 @P1 @security @automatable
  Scenario: Unauthenticated direct access to /inventory.html is blocked
    Given the user is not logged in
    When the user navigates directly to "https://www.saucedemo.com/inventory.html"
    Then the error message "Epic sadface: You can only access '/inventory.html' when you are logged in." is displayed

  @id-PV-02 @P1 @negative @automatable
  Scenario: locked_out_user cannot log in
    Given the user is on https://www.saucedemo.com
    When the user logs in as "locked_out_user" with password "secret_sauce"
    Then the error message "Epic sadface: Sorry, this user has been locked out." is displayed

  @id-PV-03 @P1 @security @automatable
  Scenario: locked_out_user stays on the login page after the failed login
    Given the user failed to log in as "locked_out_user" with password "secret_sauce"
    When the page has finished updating
    Then the URL path is "/"

  @id-PV-04 @P1 @security @automatable
  Scenario: Logout ends the session and blocks the inventory page
    Given the user is logged in as "standard_user" on "/inventory.html"
    And the user opens the burger menu and clicks "Logout"
    When the user navigates directly to "https://www.saucedemo.com/inventory.html"
    Then the error message "Epic sadface: You can only access '/inventory.html' when you are logged in." is displayed

  @id-PV-05 @P2 @positive @automatable
  Scenario: problem_user sees the same number of product cards as standard_user
    Given the user is on https://www.saucedemo.com
    When the user logs in as "problem_user" with password "secret_sauce"
    Then exactly 6 product cards are displayed

  @id-PV-06 @P3 @negative @design-only
  Scenario: problem_user behavior is compared to standard_user by manual exploration
    Given the tester is logged in as "problem_user" on "/inventory.html"
    When the tester performs sort, add to cart and remove actions on every card
    Then each deviation from the standard_user result is recorded in the defect log