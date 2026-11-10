"""Classification vocabulary. Production keyword rules belong to Phase 1."""

from compass.contracts import TransactionType

TRANSACTION_TYPES = tuple(kind.value for kind in TransactionType)
DEFAULT_TYPE = TransactionType.UNKNOWN
DEFAULT_CATEGORY = "Uncategorized"
