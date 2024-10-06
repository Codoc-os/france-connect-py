from enum import Enum


class EnumBase(str, Enum):
    """Define the base class for the enums."""

    def __str__(self) -> str:
        return str(self.value)


class Scopes(EnumBase):
    """
    Define the scopes for the France Connect API.

    For information about the relationship between scopes and claims,
    see the official documentation:
    https://docs.partenaires.franceconnect.gouv.fr/fs/fs-technique/fs-technique-scope-fc/#correspondance-entre-scope-et-claims
    """

    OPEN_ID = "openid"
    GENDER = "gender"
    BIRTH_DATE = "birthdate"
    BIRTH_COUNTRY = "birthcountry"
    BIRTH_PLACE = "birthplace"
    GIVEN_NAME = "given_name"
    FAMILY_NAME = "family_name"
    EMAIL = "email"
    PREFERRED_USERNAME = "preferred_username"
    PROFILE = "profile"
    BIRTH = "birth"
    IDENTITE_PIVOT = "identite_pivot"
    RNIPP_GIVEN_NAME = "rnipp_given_name"
    RNIPP_FAMILY_NAME = "rnipp_family_name"
    RNIPP_GENDER = "rnipp_gender"
    RNIPP_BIRTH_COUNTRY = "rnipp_birthcountry"
    RNIPP_BIRTH_PLACE = "rnipp_birthplace"
    RNIPP_BIRTH_DATE = "rnipp_birthdate"
    RNIPP_PROFILE = "rnipp_profile"
    RNIPP_BIRTH = "rnipp_birth"
    RNIPP_IDENTITE_PIVOT = "rnipp_identite_pivot"


class ACRValues(EnumBase):
    """
    Define the ACR values for the France Connect API.

    For information about the ACR values, see the official documentation:
    https://docs.partenaires.franceconnect.gouv.fr/fs/fs-technique/fs-technique-eidas-acr/
    """

    EIDAS1 = "eidas1"
    EIDAS2 = "eidas2"
    EIDAS3 = "eidas3"
