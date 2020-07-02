class Domain:
    def __init__(self):
        self._id = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _id):
        self._id = _id

    def to_dict(self):
        obj = self.__dict__.copy()
        if obj["_id"] is None:
            del obj["_id"]
        return {k[1:]: v for k, v in obj.items() if v is not None}
