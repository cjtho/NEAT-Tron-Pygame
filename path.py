import collections
import copy


class Path:
    def __init__(self):
        self.path_queue = collections.deque([])

    def add(self, item):
        item = copy.deepcopy(item)
        self.path_queue.append(item)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return list(self.path_queue)[key]
        else:
            return self.path_queue[key]

    def __iter__(self):
        return iter(self.path_queue)

    def __next__(self):
        try:
            return self.path_queue.popleft()
        except IndexError:
            raise StopIteration
