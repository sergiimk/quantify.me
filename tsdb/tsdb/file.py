from .streams import CompactStream


class TSDBFile:
    @staticmethod
    def open(path, mode='a+'):
        return TSDBFile(open(path, mode))

    def __init__(self, f):
        self.f = f

    def close(self):
        self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def read(self):
        self.f.seek(0)
        return CompactStream(self.f)

    def append(self, event):
        self.f.seek(0, 2)
        s = CompactStream(self.f)
        s.write(event)

    def clear(self):
        self.f.seek(0)
        self.f.truncate()
