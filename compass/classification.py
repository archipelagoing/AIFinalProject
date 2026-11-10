"""Transparent description rules; unmatched activity always needs review."""

from dataclasses import dataclass
import re

from compass.contracts import TransactionType, validate_cents

TRANSACTION_TYPES = tuple(kind.value for kind in TransactionType)
DEFAULT_TYPE = TransactionType.UNKNOWN
DEFAULT_CATEGORY = "Uncategorized"


@dataclass(frozen=True, slots=True)
class Classification:
    kind: TransactionType
    category: str
    explanation: str


# Ordered rules are intentionally readable and independent of evaluation labels.
EXPENSE_RULES = (
    (r"\bAPARTMENTS RENT\b", "Housing"),
    (r"\bALDI\b|\bSHOPRITE\b|\bTRADER JOES\b", "Groceries"),
    (r"\bTHAI BASIL\b|\bSUSHI MARKET\b|\bCHIPOTLE\b|\bSTARBUCKS\b", "Restaurants"),
    (r"\bUTILITIES\b", "Utilities"), (r"\bVERIZON\b", "Phone"),
    (r"\bCOMCAST\b", "Internet"), (r"\bGEICO\b", "Insurance"),
    (r"\bWAWA FUEL\b|\bSHELL GAS\b", "Transportation"),
    (r"\bNETFLIX\b|\bSPOTIFY\b", "Subscriptions"),
    (r"\bPLANET FITNESS\b", "Fitness"), (r"\bCVS PHARMACY\b", "Health"),
    (r"\bAMAZON\b", "Shopping"), (r"\bCAR REPAIR\b", "Auto maintenance"),
    (r"\bSTUDENT LOAN\b", "Debt payment"),
)


def classify(description: str, amount_cents: int) -> Classification:
    validate_cents(amount_cents)
    text = description.upper()
    if re.search(r"\bSAVINGS TRANSFER\b", text):
        return Classification(TransactionType.TRANSFER, "Transfer", "Description identifies a savings transfer; exclude from income and spending.")
    if re.search(r"\bVENMO FRIEND DINNER (SPLIT|REIMBURSEMENT)\b", text):
        return Classification(TransactionType.TRANSFER, "Transfer", "Peer dinner transfer, not wages. Confirm this rule's interpretation during review.")
    if amount_cents > 0 and re.search(r"\bPAYROLL\b|\bFREELANCE\b", text):
        return Classification(TransactionType.INCOME, "Income", "Positive payroll or freelance payment.")
    if amount_cents > 0 and re.search(r"\bSHOPRITE RETURN\b", text):
        return Classification(TransactionType.REFUND, "Groceries", "Positive grocery return reduces net grocery expenses, not earned income.")
    if amount_cents < 0:
        for pattern, category in EXPENSE_RULES:
            if re.search(pattern, text):
                return Classification(TransactionType.EXPENSE, category, f"Negative purchase matched description rule: {pattern}")
    return Classification(DEFAULT_TYPE, DEFAULT_CATEGORY, "No reliable rule matched. Exclude from verified totals until reviewed.")
