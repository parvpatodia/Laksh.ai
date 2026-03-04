from __future__ import annotations

from typing import Any, Iterable, List

class DummyPipeline:
    def run(self, inputs: Iterable[Any]) -> List[Any]:
        return list(inputs)
