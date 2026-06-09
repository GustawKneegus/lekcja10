"""Data models for the apartment management system."""

import json

from pydantic import BaseModel


class Parameters(BaseModel):
    """Application configuration parameters.

    Attributes
    ----------
    apartments_json_path : str
        Path to apartment definitions.

    tenants_json_path : str
        Path to tenant records.

    transfers_json_path : str
        Path to transfer history.

    bills_json_path : str
        Path to bills data.

    tenants_blacklist_json_path : str
        Path to tenant blacklist entries.

    apartment_events_json_path : str
        Path to apartment event records.

    max_transfer_pln : float
        Maximum allowed transfer amount.

    max_refund_pln : float
        Maximum allowed refund amount.

    """

    apartments_json_path: str = "data/apartments.json"
    tenants_json_path: str = "data/tenants.json"
    transfers_json_path: str = "data/transfers.json"
    bills_json_path: str = "data/bills.json"
    tenants_blacklist_json_path: str = "data/tenants_blacklist.json"
    apartment_events_json_path: str = "data/apartment_events.json"

    max_transfer_pln: float = 4500.0
    max_refund_pln: float = 2500.0


class Room(BaseModel):
    """A room model in the apartment."""

    name: str
    area_m2: float


class Apartment(BaseModel):
    """Represents an apartment available for rent.

    Attributes
    ----------
    key : str
        Unique apartment identifier.

    name : str
        Human-readable apartment name.

    location : str
        Physical address or location description.

    area_m2 : float
        Total apartment area in square meters.

    rooms : Dict[str, Room]
        Mapping of room identifiers to room definitions.

    """

    key: str
    name: str
    location: str
    area_m2: float
    rooms: dict[str, Room]

    @staticmethod
    def from_json_file(file_path: str) -> dict[str, "Apartment"]:
        """Load apartment definitions from a JSON file.

        Parameters
        ----------
        file_path : str
        Path to the JSON file containing apartment data.

        Returns
        -------
        Dict[str, Apartment]
        Dictionary where keys are apartment identifiers and
        values are Apartment objects.

        Raises
        ------
        AssertionError
        If the JSON root element is not a dictionary.

        """
        """
        Example:
        ----
            >>> apartments = Apartment.from_json_file('data/apartments.json')
            >>> isinstance(apartments, dict)
            True
        """
        data = None
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of apartments"
        return {key: Apartment(**apartment) for key, apartment in data.items()}


class Tenant(BaseModel):
    """Represents a tenant renting a room in an apartment.

    Attributes
    ----------
    name : str
        Full name or identifier of the tenant.

    apartment : str
        Key of the apartment occupied by the tenant.

    room : str
        Room identifier within the apartment.

    rent_pln : float
        Monthly rent amount in PLN.

    deposit_pln : float
        Security deposit paid by the tenant.

    date_agreement_from : str
        Rental agreement start date (YYYY-MM-DD).

    date_agreement_to : str
        Rental agreement end date (YYYY-MM-DD).

    """

    name: str
    apartment: str
    room: str
    rent_pln: float
    deposit_pln: float
    date_agreement_from: str
    date_agreement_to: str

    @staticmethod
    def from_json_file(file_path: str) -> dict[str, "Tenant"]:
        """Load tenants from a JSON file and return a dictionary of Tenant instances.

        Example:
        -------
            >>> tenants = Tenant.from_json_file('data/tenants.json')
            >>> isinstance(tenants, dict)
            True

        """
        data = None
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of tenants"
        return {key: Tenant(**tenant) for key, tenant in data.items()}


class TenantBlacklistEntry(BaseModel):
    """A blacklist entry for a tenant in the apartment management system."""

    tenant: str
    reason: str

    @staticmethod
    def from_json_file(file_path: str) -> list["TenantBlacklistEntry"]:
        """Load tenant blacklist entries from a JSON file.

        Example:
        -------
            >>> blacklist = TenantBlacklistEntry.from_json_file('data/tenants_blacklist.json')
            >>> isinstance(blacklist, list)
            True

        """
        data = None
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        assert isinstance(data, list), "Expected a list of blacklist entries"
        return [TenantBlacklistEntry(**entry) for entry in data]


class Transfer(BaseModel):
    """A transfer model representing a financial transaction in the apartment management system."""

    amount_pln: float
    date: str
    settlement_year: int | None
    settlement_month: int | None
    tenant: str
    type: str | None = None

    @staticmethod
    def from_json_file(file_path: str) -> list["Transfer"]:
        """Load transfers from a JSON file and return a list of Transfer instances.

        Example:
        -------
            >>> transfers = Transfer.from_json_file('data/transfers.json')
            >>> isinstance(transfers, list)
            True

        """
        data = None
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        assert isinstance(data, list), "Expected a list of transfers"
        return [Transfer(**transfer) for transfer in data]


class Bill(BaseModel):
    """A bill model representing a financial obligation in the apartment management system."""

    amount_pln: float
    date_due: str
    apartment: str
    settlement_year: int
    settlement_month: int
    type: str

    @staticmethod
    def from_json_file(file_path: str) -> list["Bill"]:
        """Load bills from a JSON file and return a list of Bill instances.

        Example:
        -------
            >>> bills = Bill.from_json_file('data/bills.json')
            >>> isinstance(bills, list)
            True

        """
        data = None
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        assert isinstance(data, list), "Expected a list of bills"
        return [Bill(**bill) for bill in data]


class ApartmentSettlement(BaseModel):
    """An apartment settlement model representing the financial summary for an apartment
    in a given month and year.
    """

    key: str
    apartment: str
    month: int
    year: int
    total_due_pln: float
    total_transfers_pln: float = 0.0
    balance_pln: float = 0.0


class TenantSettlement(BaseModel):
    """A tenant settlement model representing the financial summary for a tenant
    in a given month and year.
    """

    tenant: str
    apartment_settlement: str
    month: int
    year: int
    total_due_pln: float
    total_transfers_pln: float = 0.0
    balance_pln: float = 0.0


class ApartmentEvent(BaseModel):
    """An apartment event model representing an event or issue related to an apartment."""

    date: str
    apartment: str
    amount_pln: float | None = None
    tenant: str | None = None
    description: str
    solved: bool = False

    @staticmethod
    def from_json_file(file_path: str) -> list["ApartmentEvent"]:
        """Load apartment events from a JSON file.

        Example:
        -------
            >>> events = ApartmentEvent.from_json_file('data/apartment_events.json')
            >>> isinstance(events, list)
            True

        """
        data = None
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        assert isinstance(data, list), "Expected a list of apartment events"
        return [ApartmentEvent(**event) for event in data]
