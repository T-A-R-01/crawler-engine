from collections import deque


class URLScheduler:
    def __init__(self):
        self.queue = deque()
        self.visited = set()

    def add_url(self, url):
        if url not in self.visited and url not in self.queue:
            self.queue.append(url)

    def get_url(self):
        if self.queue:
            url = self.queue.popleft()
            self.visited.add(url)
            return url
        return None

    def has_urls(self):
        return len(self.queue) > 0