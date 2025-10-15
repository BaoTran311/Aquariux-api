from src.utils import Dotdict


class DataRuntime:
    option: Dotdict
    config: Dotdict

    @classmethod
    def is_demo(cls):
        return cls.option.account.lower() == "demo"  # noqa

    @classmethod
    def is_live(cls):
        cls.option.account.lower() == "live"  # noqa

    @classmethod
    def is_crm(cls):
        cls.option.account.lower() == "crm"  # noqa

    @classmethod
    def is_mt4(cls):
        return cls.option.server == "mt4"

    @classmethod
    def is_mt5(cls):
        return cls.option.server == "mt5"
