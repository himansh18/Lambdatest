Feature: REST API test design

  # DESIGN ONLY: Assumed endpoints and expected statuses.
  # Confirm all assumptions against the actual API specification.
  # These scenarios have not been executed against a real API.

  Background:
    Given a hypothetical resource-management REST API
    And the API contract is not yet available

  @auth @positive
  Scenario: Accept a valid authentication token
    Given a valid, unexpired token
    When the client requests GET /api/v1/resources
    Then the expected status is 200
    And the response contains the permitted resource collection

  @auth @negative
  Scenario Outline: Reject invalid authentication credentials
    Given the request uses a "<token_state>" token
    When the client requests GET /api/v1/resources
    Then the expected status is 401

    Examples:
      | token_state |
      | missing     |
      | malformed   |
      | expired     |

  @auth @security
  Scenario: Reject insufficient permissions
    Given an authenticated user without resource-delete permission
    When the client requests DELETE /api/v1/resources/123
    Then the expected status is 403

  @crud @positive
  Scenario: Create a resource
    Given an authenticated client with create permission
    When the client sends POST /api/v1/resources with valid resource data
    Then the expected status is 201
    And the response contains the created resource identifier

  @crud @positive
  Scenario: Retrieve an existing resource
    Given resource 123 exists
    When the client requests GET /api/v1/resources/123
    Then the expected status is 200
    And the response conforms to the resource schema

  @crud @positive
  Scenario: Update an existing resource
    Given resource 123 exists
    When the client sends PUT /api/v1/resources/123 with valid replacement data
    Then the expected status is 200 or 204 according to the API contract

  @crud @positive
  Scenario: Partially update an existing resource
    Given resource 123 exists
    When the client sends PATCH /api/v1/resources/123 with one valid field
    Then the expected status is 200 or 204 according to the API contract
    And unspecified fields remain unchanged

  @crud @positive
  Scenario: Delete an existing resource
    Given resource 123 exists
    When the client sends DELETE /api/v1/resources/123
    Then the expected status is 204 or another documented success status
    And a subsequent retrieval confirms the documented deletion behavior

  @crud @negative
  Scenario: Retrieve a nonexistent resource
    Given resource 999999 does not exist
    When the client requests GET /api/v1/resources/999999
    Then the expected status is 404

  @errors @negative
  Scenario: Reject malformed JSON
    Given an authenticated client
    When the client submits malformed JSON to POST /api/v1/resources
    Then the expected status is 400 or the documented validation status
    And the response contains a structured error

  @errors @negative
  Scenario: Reject missing required fields
    Given an authenticated client
    When the client creates a resource without a required field
    Then the expected status is 400 or 422 according to the API contract

  @errors @negative
  Scenario: Reject an unsupported HTTP method
    Given an existing resource endpoint
    When the client uses an unsupported HTTP method
    Then the expected status is 405

  @errors @resilience
  Scenario: Handle an internal server error
    Given the test environment can safely simulate a server error
    When the request triggers the documented error condition
    Then the expected status is 500
    And the response does not expose stack traces or secrets

  @rate_limit @positive
  Scenario: Stay within the rate limit
    Given the client has remaining request quota
    When the client sends requests within the documented limit
    Then the requests receive the documented success responses

  @rate_limit @negative
  Scenario: Exceed the rate limit
    Given the client is subject to a documented rate limit
    When the client exceeds the allowed request quota
    Then the expected status is 429
    And rate-limit headers and retry guidance follow the API contract

  @schema @negative
  Scenario Outline: Reject invalid resource field values
    Given an authenticated client
    When the client submits a resource with "<invalid_value>"
    Then the response follows the documented schema-validation error contract

    Examples:
      | invalid_value       |
      | wrong data type     |
      | invalid date format |
      | null required field |
      | unexpected field    |

  @schema @positive
  Scenario: Validate a successful response schema
    Given a valid resource exists
    When the client requests GET /api/v1/resources/123
    Then required response fields are present
    And each field has the documented data type and format