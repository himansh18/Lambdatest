Feature: REST API test design (JSONPlaceholder as the stand-in API)

  # SCOPE: Scenarios tagged @implemented are covered by tests/api/test_rest_api.py against
  # https://jsonplaceholder.typicode.com and were observed passing on 2026-10-23.
  # Scenarios tagged @design-only could not be run against JSONPlaceholder (it has no auth,
  # no rate limiting and does not validate input). Their endpoint /api/v1/resources and their
  # statuses are EXAMPLES that must be confirmed against a real API contract.
  # Every Then step asserts exactly one outcome.

  Background:
    Given the API base URL is "https://jsonplaceholder.typicode.com"

  # ---------- Authentication and token validation (design only) ----------

  # Objective: a valid token is accepted
  # Preconditions: a valid, unexpired token exists. Request data: header "Authorization: Bearer <valid_token>"
  @id-API-01 @P1 @positive @auth @design-only
  Scenario: Accept a valid authentication token
    Given a valid, unexpired token
    When the client sends GET /api/v1/resources
    Then the response status is 200

  # Objective: a request without a usable token is rejected
  # Preconditions: none. Request data: token state as listed in Examples
  @id-API-02 @P1 @negative @auth @design-only
  Scenario Outline: Reject a missing, malformed or expired token
    Given the request uses a "<token_state>" token
    When the client sends GET /api/v1/resources
    Then the response status is 401

    Examples:
      | token_state |
      | missing     |
      | malformed   |
      | expired     |

  # Objective: a user without delete permission cannot delete
  # Preconditions: authenticated user with the read-only role. Request data: resource id 123
  @id-API-03 @P1 @security @auth @design-only
  Scenario: Reject a delete from a user without delete permission
    Given an authenticated user with the read-only role
    When the client sends DELETE /api/v1/resources/123
    Then the response status is 403

  # ---------- CRUD operations (implemented on JSONPlaceholder /posts) ----------

  # Objective: the list endpoint returns posts
  # Preconditions: none. Request data: none
  @id-API-04 @P1 @positive @crud @implemented
  Scenario: Retrieve the list of posts
    When the client sends GET /posts
    Then the response status is 200
    And the response body is a JSON list

  # Objective: a single post matches the expected schema
  # Preconditions: post 1 exists. Request data: none
  @id-API-05 @P1 @positive @crud @schema @implemented
  Scenario: Retrieve post 1 with the expected fields and types
    When the client sends GET /posts/1
    Then the response status is 200
    And the response has integer fields "userId" and "id" and string fields "title" and "body"

  # Objective: a new post can be created
  # Preconditions: none. Request data: {"title": "foo", "body": "bar", "userId": 1}
  @id-API-06 @P1 @positive @crud @implemented
  Scenario: Create a post
    When the client sends POST /posts with {"title": "foo", "body": "bar", "userId": 1}
    Then the response status is 201
    And the response contains an "id" field

  # Objective: a post can be fully replaced
  # Preconditions: post 1 exists. Request data: {"id": 1, "title": "updated", "body": "bar", "userId": 1}
  @id-API-07 @P1 @positive @crud @implemented
  Scenario: Replace post 1 with PUT
    When the client sends PUT /posts/1 with {"id": 1, "title": "updated", "body": "bar", "userId": 1}
    Then the response status is 200
    And the response field "title" equals "updated"

  # Objective: a single field of a post can be changed
  # Preconditions: post 1 exists. Request data: {"title": "patched"}
  @id-API-08 @P2 @positive @crud @implemented
  Scenario: Partially update post 1 with PATCH
    When the client sends PATCH /posts/1 with {"title": "patched"}
    Then the response status is 200
    And the response field "title" equals "patched"

  # Objective: a post can be deleted
  # Preconditions: post 1 exists. Request data: none
  @id-API-09 @P2 @positive @crud @implemented
  Scenario: Delete post 1
    When the client sends DELETE /posts/1
    Then the response status is 200

  # Objective: a missing post returns 404 (observed behaviour; an earlier assumption of 200 was wrong)
  # Preconditions: post 999999 does not exist. Request data: none
  @id-API-10 @P1 @negative @crud @implemented
  Scenario: Retrieve a nonexistent post
    When the client sends GET /posts/999999
    Then the response status is 404

  # ---------- Error handling (design only) ----------

  # Objective: malformed JSON is rejected
  # Preconditions: authenticated client. Request data: body {"title": "foo"  (missing closing brace)
  @id-API-11 @P1 @negative @errors @design-only
  Scenario: Reject malformed JSON
    Given an authenticated client
    When the client sends POST /api/v1/resources with the body '{"title": "foo"'
    Then the response status is 400

  # Objective: the error response has a consistent structure
  # Preconditions: authenticated client. Request data: same malformed body as API-11
  @id-API-12 @P2 @negative @errors @design-only
  Scenario: Error responses use a consistent JSON structure
    Given an authenticated client
    When the client sends POST /api/v1/resources with the body '{"title": "foo"'
    Then the response body contains the fields "code" and "message"

  # Objective: a missing required field is rejected
  # Preconditions: authenticated client. Request data: {"body": "bar"} (no "title")
  @id-API-13 @P1 @negative @errors @design-only
  Scenario: Reject a missing required field
    Given an authenticated client
    When the client sends POST /api/v1/resources with {"body": "bar"}
    Then the response status is 422

  # Objective: an unsupported HTTP method is rejected
  # Preconditions: resource 123 exists. Request data: none
  @id-API-14 @P2 @negative @errors @design-only
  Scenario: Reject an unsupported HTTP method
    Given resource 123 exists
    When the client sends TRACE /api/v1/resources/123
    Then the response status is 405

  # Objective: a server error does not leak internals
  # Preconditions: test environment can safely trigger a 500. Request data: the documented error trigger
  @id-API-15 @P2 @security @errors @design-only
  Scenario: Server error response hides stack traces
    Given the test environment can safely trigger a server error
    When the client sends the documented error-trigger request
    Then the response body does not contain the text "Traceback"

  # ---------- Rate limiting (design only) ----------

  # Objective: requests inside the limit succeed
  # Preconditions: documented limit of 100 requests per minute. Request data: 50 GET requests in one minute
  @id-API-16 @P2 @positive @rate-limit @design-only
  Scenario: Stay within the rate limit
    Given the documented limit is 100 requests per minute
    When the client sends 50 GET requests to /api/v1/resources within one minute
    Then every response status is 200

  # Objective: requests over the limit are throttled
  # Preconditions: same limit. Request data: 101 GET requests in one minute
  @id-API-17 @P1 @negative @rate-limit @design-only
  Scenario: Exceed the rate limit
    Given the documented limit is 100 requests per minute
    When the client sends 101 GET requests to /api/v1/resources within one minute
    Then the 101st response status is 429

  # Objective: the throttled response tells the client when to retry
  # Preconditions: client is over the limit. Request data: one more GET request
  @id-API-18 @P2 @negative @rate-limit @design-only
  Scenario: Throttled response includes a Retry-After header
    Given the client has exceeded the rate limit
    When the client sends GET /api/v1/resources
    Then the response contains the header "Retry-After"

  # ---------- Schema validation (design only) ----------

  # Objective: invalid field values are rejected with a validation status
  # Preconditions: authenticated client. Request data: one invalid value per row
  @id-API-19 @P1 @negative @schema @design-only
  Scenario Outline: Reject an invalid field value
    Given an authenticated client
    When the client sends POST /api/v1/resources with the invalid value "<invalid_value>"
    Then the response status is 422

    Examples:
      | invalid_value                      |
      | {"title": 123}                     |
      | {"title": "foo", "createdAt": "31-31-2026"} |
      | {"title": null}                    |

  # Objective: unexpected fields are rejected
  # Preconditions: authenticated client. Request data: {"title": "foo", "isAdmin": true}
  @id-API-20 @P2 @security @schema @design-only
  Scenario: Reject an unexpected field
    Given an authenticated client
    When the client sends POST /api/v1/resources with {"title": "foo", "isAdmin": true}
    Then the response status is 422
