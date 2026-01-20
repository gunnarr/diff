"""Rate limiter for scrapers."""
import asyncio
from collections import defaultdict
from typing import Dict


class RateLimiter:
    """Rate limiter to control request frequency per source."""

    def __init__(self):
        self.last_request: Dict[str, float] = defaultdict(float)
        self.delays: Dict[str, float] = {
            'svt': 5.0,         # SVT: 5 seconds (respectful, public service)
            'dn': 3.0,          # DN: 3 seconds
            'svd': 3.0,         # SVD: 3 seconds
            'aftonbladet': 2.0,  # Aftonbladet: 2 seconds
            'expressen': 2.0,    # Expressen: 2 seconds
        }

    async def wait(self, source_key: str):
        """Wait appropriate time before next request to source."""
        loop = asyncio.get_event_loop()
        now = loop.time()
        last = self.last_request[source_key]
        delay = self.delays.get(source_key, 3.0)

        if now - last < delay:
            wait_time = delay - (now - last)
            await asyncio.sleep(wait_time)

        self.last_request[source_key] = loop.time()
