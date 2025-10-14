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
