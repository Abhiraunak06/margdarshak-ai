from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime

class BaseExamAdapter(ABC):
    """
    Abstract base class for all examination data ingestion adapters.
    Each exam (JEE Main, JEE Advanced, WBJEE, COMEDK, MHT CET, etc.) implements this interface.
    """
    def __init__(self, exam_code: str, name: str, source_url: str):
        self.exam_code = exam_code
        self.name = name
        self.source_url = source_url

    @abstractmethod
    def fetch_raw(self, year: int, round_no: int = None) -> List[Dict[str, Any]]:
        """Fetch raw records from authoritative source (API, file, or remote dataset)."""
        pass

    @abstractmethod
    def parse_and_normalize(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize institutes, branches, categories, quotas, genders, ranks."""
        pass

    @abstractmethod
    def sync(self, db_session, year: int, rounds: List[int] = None) -> Dict[str, Any]:
        """Execute full synchronization pipeline, validate records, insert to DB, and log results."""
        pass

    def get_source_metadata(self) -> Dict[str, Any]:
        return {
            "exam_code": self.exam_code,
            "name": self.name,
            "source_url": self.source_url,
            "last_checked": datetime.utcnow().isoformat()
        }
