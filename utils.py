class AdditiveUpdateDict(dict):
    def update(self, other):
        for key, val in other.items():
            if isinstance(val, (dict,)) and isinstance(self[key], (self.__class__,)):
                self[key].update(val)
            elif isinstance(val, (list,)) and isinstance(self[key], (list,)):
                self[key].extend(val)
            else:
                try:
                    self[key] += val
                except KeyError:
                    self[key] = val
        # return self
