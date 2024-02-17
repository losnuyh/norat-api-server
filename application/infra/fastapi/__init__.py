class WithFastAPIRouter:
    def start(self):
        for item in self.__dir__():
            if not item.startswith("_") and item != "start":
                target = getattr(self, item)
                if hasattr(target, "__self__") and target.__self__ == self:
                    target()
