import pytest
from classes.email import Email, EmailTypes

# Test IDs for parametrization
HAPPY_PATH_ID = "happy_path"
EDGE_CASE_ID = "edge_case"
ERROR_CASE_ID = "error_case"

# Happy path test values
happy_path_params = [
    (
        "jane.doe@example.com",
        EmailTypes.PERSONAL,
        "example",
        "Personal: jane.doe@example.com",
    ),
    (
        "john.doe@business.net",
        EmailTypes.BUSINESS,
        "business",
        "Business: john.doe@business.net",
    ),
    ("info@other.org", EmailTypes.OTHER, "other", "Other: info@other.org"),
]

# Edge case test values
edge_case_params = [
    (
        "",
        EmailTypes.PERSONAL,
        "unknown",
        "Personal: defEmail@test.com",
    ),  # Empty email address
    (
        "no-at-symbol",
        EmailTypes.BUSINESS,
        "unknown",
        "Business: defEmail@test.com",
    ),  # No @ symbol
    (
        "@no-domain",
        EmailTypes.OTHER,
        "unknown",
        "Other: defEmail@test.com",
    ),  # No domain after @
    (
        "just@domain.",
        EmailTypes.PERSONAL,
        "domain",
        "Personal: defEmail@test.com",
    ),  # No TLD after domain
]

# Error case test values
error_case_params = [
    (None, EmailTypes.PERSONAL, TypeError),  # None as email address
    (123, EmailTypes.BUSINESS, TypeError),  # Non-string email address
]


@pytest.mark.parametrize(
    "address, email_type, expected_domain, expected_repr",
    happy_path_params,
    ids=[HAPPY_PATH_ID] * len(happy_path_params),
)
def test_email_happy_path(address, email_type, expected_domain, expected_repr):
    # Arrange
    email = Email(address=address, type=email_type)

    # Act
    domain = email.domain
    repr_string = repr(email)

    # Assert
    assert (
        domain == expected_domain
    ), f"Expected domain '{expected_domain}', got '{domain}'"
    assert (
        repr_string == expected_repr
    ), f"Expected representation '{expected_repr}', got '{repr_string}'"


@pytest.mark.parametrize(
    "address, email_type, expected_domain, expected_repr",
    edge_case_params,
    ids=[EDGE_CASE_ID] * len(edge_case_params),
)
def test_email_edge_cases(address, email_type, expected_domain, expected_repr):
    # Arrange
    email = Email(address=address, type=email_type)

    # Act
    domain = email.domain
    repr_string = repr(email)

    # Assert
    assert (
        domain == expected_domain
    ), f"Expected domain '{expected_domain}', got '{domain}'"
    assert (
        repr_string == expected_repr
    ), f"Expected representation '{expected_repr}', got '{repr_string}'"


@pytest.mark.parametrize(
    "address, email_type, expected_exception",
    error_case_params,
    ids=[ERROR_CASE_ID] * len(error_case_params),
)
def test_email_error_cases(address, email_type, expected_exception):
    # Act / Assert
    with pytest.raises(expected_exception):
        Email(address=address, type=email_type)
