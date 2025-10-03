from src.enums import BaseEnum


class Clients(BaseEnum):
    LIRUNEX = "lirunex"
    TRANSACTCLOUD = "transactCloud"


class AccountType(BaseEnum):
    DEMO = "demo"
    LIVE = "live"
    CRM = "crm"
