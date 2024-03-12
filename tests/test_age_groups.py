import pytest
from classes.age_groups import AgeGroups


# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "age, expected_group",
    [
        (0, AgeGroups.INFANT),  # ID: test_infant_lower_bound
        (1, AgeGroups.INFANT),  # ID: test_infant_within_range
        (2, AgeGroups.TODDLER),  # ID: test_toddler_lower_bound
        (3, AgeGroups.TODDLER),  # ID: test_toddler_within_range
        (4, AgeGroups.EARLY_CHILDHOOD),  # ID: test_early_childhood_lower_bound
        (7, AgeGroups.EARLY_CHILDHOOD),  # ID: test_early_childhood_within_range
        (8, AgeGroups.LATE_CHILDHOOD),  # ID: test_late_childhood_lower_bound
        (10, AgeGroups.LATE_CHILDHOOD),  # ID: test_late_childhood_within_range
        (11, AgeGroups.EARLY_TEEN),  # ID: test_early_teen_lower_bound
        (14, AgeGroups.EARLY_TEEN),  # ID: test_early_teen_within_range
        (15, AgeGroups.LATE_TEEN),  # ID: test_late_teen_lower_bound
        (19, AgeGroups.LATE_TEEN),  # ID: test_late_teen_within_range
        (20, AgeGroups.EARLY_YOUNG_ADULT),  # ID: test_early_young_adult_lower_bound
        (29, AgeGroups.EARLY_YOUNG_ADULT),  # ID: test_early_young_adult_within_range
        (30, AgeGroups.LATE_YOUNG_ADULT),  # ID: test_late_young_adult_lower_bound
        (39, AgeGroups.LATE_YOUNG_ADULT),  # ID: test_late_young_adult_within_range
        (40, AgeGroups.MIDDLE_AGE),  # ID: test_middle_age_lower_bound
        (59, AgeGroups.MIDDLE_AGE),  # ID: test_middle_age_within_range
        (60, AgeGroups.SENIOR),  # ID: test_senior_lower_bound
        (79, AgeGroups.SENIOR),  # ID: test_senior_within_range
        (80, AgeGroups.LATE_SENIOR),  # ID: test_late_senior_lower_bound
        (119, AgeGroups.LATE_SENIOR),  # ID: test_late_senior_within_range
    ],
)
def test_age_group_contains(age, expected_group):
    # Act
    result = AgeGroups.contains(age)

    # Assert
    assert result == expected_group, f"Age {age} should be in {expected_group}"


# Edge cases
@pytest.mark.parametrize(
    "age, expected_group",
    [
        (2, AgeGroups.TODDLER),  # ID: test_edge_case_toddler
        (4, AgeGroups.EARLY_CHILDHOOD),  # ID: test_edge_case_early_childhood
        (11, AgeGroups.EARLY_TEEN),  # ID: test_edge_case_early_teen
        (15, AgeGroups.LATE_TEEN),  # ID: test_edge_case_late_teen
        (20, AgeGroups.EARLY_YOUNG_ADULT),  # ID: test_edge_case_early_young_adult
        (30, AgeGroups.LATE_YOUNG_ADULT),  # ID: test_edge_case_late_young_adult
        (40, AgeGroups.MIDDLE_AGE),  # ID: test_edge_case_middle_age
        (60, AgeGroups.SENIOR),  # ID: test_edge_case_senior
        (80, AgeGroups.LATE_SENIOR),  # ID: test_edge_case_late_senior
        (120, None),  # ID: test_edge_case_beyond_late_senior
    ],
)
def test_age_group_edge_cases(age, expected_group):
    # Act
    result = AgeGroups.contains(age)

    # Assert
    assert result == expected_group, f"Age {age} should be in {expected_group}"


# Error cases
@pytest.mark.parametrize(
    "age",
    [
        (-1),  # ID: test_error_negative_age
        (121),  # ID: test_error_beyond_defined_range
        ("ten"),  # ID: test_error_non_numeric_age
        (None),  # ID: test_error_none_age
    ],
)
def test_age_group_error_cases(age):
    # Act
    # if isinstance(age, int):
    result = AgeGroups.contains(age)
    # else:
    #     with pytest.raises(TypeError):
    #         result = AgeGroups.contains(age)
    #         return

    # Assert
    assert result is None, f"Age {age} should not be in any age group"
