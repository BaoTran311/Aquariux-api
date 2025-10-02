from src.core.request import XRequest


class BaseAPI:
    def __init__(self):
        super().__init__()
        self.request = XRequest()

    # def __getattr__(self, name):
    #     return getattr(self.request, name)
    #
    # def __dir__(self):
    #     return super().__dir__() + dir(self.request)
