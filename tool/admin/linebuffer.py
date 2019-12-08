

class LineBuffer:

    def __init__(self):
        self._curr_size = 0
        self._buf = []

    def __len__(self):
        return self._curr_size

