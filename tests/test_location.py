import pytest
from classes.location import Location, LocationTypes, HomeTypes, BusinessTypes


@pytest.mark.parametrize(
    "id, street_address_1, street_address_2, city, state, zipcode, country, loc_type, subtype, expected_repr, expected_state_abbr, expected_address",
    [
        # Happy path tests
        (
            "HP-1",
            "123 Main St",
            "Apt 4",
            "Anytown",
            "California",
            "12345",
            "USA",
            LocationTypes.HOME,
            HomeTypes.APARTMENT,
            "Home: 123 Main St - Apt 4, Anytown, CA - 12345",
            "CA",
            "123 Main St - Apt 4, Anytown, CA - 12345",
        ),
        (
            "HP-2",
            "456 Elm St",
            "",
            "Otherville",
            "DefaultState",
            "67890",
            "USA",
            LocationTypes.BUSINESS,
            BusinessTypes.HQ,
            "Business: 456 Elm St, Otherville, DS - 67890",
            "DS",
            "456 Elm St, Otherville, DS - 67890",
        ),
        # Edge cases
        (
            "EC-1",
            "",
            "",
            "",
            "California",
            "",
            "USA",
            LocationTypes.OTHER,
            None,
            "Other: '', California, CA - ",
            "",
            ", California, CA - ",
        ),
        # Error cases
        (
            "ER-1",
            "789 Oak St",
            None,
            "Sometown",
            "NonExistentState",
            "99999",
            "USA",
            LocationTypes.HOME,
            HomeTypes.OTHER,
            "Home: 789 Oak St, Sometown, - 99999",
            None,
            "789 Oak St, Sometown, NonExistentState - 99999",
        ),
    ],
)
def test_location_repr_state_abbr_address(
    id,
    street_address_1,
    street_address_2,
    city,
    state,
    zipcode,
    country,
    loc_type,
    subtype,
    expected_repr,
    expected_state_abbr,
    expected_address,
):
    # Arrange
    location = Location(
        street_address_1=street_address_1,
        street_address_2=street_address_2,
        city=city,
        state=state,
        zipcode=zipcode,
        country=country,
        loc_type=loc_type,
        subtype=subtype,
    )

    # Act
    actual_repr = repr(location)
    actual_state_abbr = location.state_abbr
    actual_address = location.address

    # Assert
    assert (
        actual_repr == expected_repr
    ), f"Test ID: {id} - repr does not match expected value"
    assert (
        actual_state_abbr == expected_state_abbr
    ), f"Test ID: {id} - state abbreviation does not match expected value"
    assert (
        actual_address == expected_address
    ), f"Test ID: {id} - address does not match expected value"


# Additional tests should be written to cover __getitem__ and other edge cases or error cases as needed.
