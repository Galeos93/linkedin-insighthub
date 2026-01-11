import re
from typing import List


class SimpleTokenizer:
    def tokenize(self, text: str) -> List[str]:
        text = text.lower()
        return re.findall(r"[a-z0-9]{2,}", text)
