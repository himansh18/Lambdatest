from ai.failure_explainer import redact_sensitive_text


def test_redact_sensitive_text_removes_common_credentials() -> None:
    text = "API_KEY=abc123 password: hunter2 Authorization: token-value Bearer jwt.token"

    redacted = redact_sensitive_text(text)

    assert "abc123" not in redacted
    assert "hunter2" not in redacted
    assert "token-value" not in redacted
    assert "jwt.token" not in redacted
    assert redacted.count("[REDACTED]") == 4
