from dataclasses import dataclass
from typing import Optional

@dataclass
class QualityIssue:
    issue_type: str
    column: Optional[str]
    description: str
    affected_rows: int
