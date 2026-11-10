"""Explicit CSV interpretation. Never infer amount polarity or date order."""

from dataclasses import asdict, dataclass
from datetime import datetime
import json

from compass.contracts import parse_amount_cents, validate_cents, validate_posted_date


@dataclass(frozen=True, slots=True, kw_only=True)
class ColumnMapping:
    date_column: str
    description_column: str
    amount_mode: str
    account_column: str | None = None
    fixed_account: str | None = None
    transaction_id_column: str | None = None
    amount_column: str | None = None
    debit_column: str | None = None
    credit_column: str | None = None
    date_format: str = "%Y-%m-%d"

    def validate(self, headers: list[str]) -> None:
        if self.amount_mode not in {"inflow_positive", "outflow_positive", "debit_credit"}:
            raise ValueError("Explicitly choose signed inflows, signed outflows, or separate debit/credit columns.")
        if self.date_format not in {"%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"}:
            raise ValueError("Choose an explicit supported date format.")
        if bool(self.account_column) == bool(self.fixed_account and self.fixed_account.strip()):
            raise ValueError("Choose either an account column or one fixed account name.")
        if self.amount_mode == "debit_credit":
            if not self.debit_column or not self.credit_column or self.amount_column:
                raise ValueError("Map separate debit and credit columns, with no signed-amount column.")
            money_columns = [self.debit_column, self.credit_column]
        else:
            if not self.amount_column or self.debit_column or self.credit_column:
                raise ValueError("Map one signed-amount column, with no debit/credit columns.")
            money_columns = [self.amount_column]
        columns = [self.date_column, self.description_column, *money_columns]
        columns += [column for column in (self.account_column, self.transaction_id_column) if column]
        if any(not column or column not in headers for column in columns):
            raise ValueError("Every selected field must refer to an existing CSV column.")
        if len(set(columns)) != len(columns):
            raise ValueError("Use a different source column for each mapped field.")

    def normalize(self, raw: dict[str, str]) -> dict[str, str | int | None]:
        text_date = raw[self.date_column].strip()
        if self.date_format == "%Y-%m-%d":
            posted_date = validate_posted_date(text_date)
        else:
            parsed = datetime.strptime(text_date, self.date_format)
            if parsed.strftime(self.date_format) != text_date:
                raise ValueError("Date must exactly match the explicitly selected format.")
            posted_date = parsed.date().isoformat()
        if self.amount_mode == "debit_credit":
            debit_text, credit_text = raw[self.debit_column].strip(), raw[self.credit_column].strip()
            if not debit_text and not credit_text:
                raise ValueError("Provide a debit or a credit value; both columns are blank.")
            debit = parse_amount_cents(debit_text) if debit_text else 0
            credit = parse_amount_cents(credit_text) if credit_text else 0
            if debit < 0 or credit < 0 or (debit and credit):
                raise ValueError("Debit/credit values must be nonnegative and cannot both be nonzero in one row.")
            amount = validate_cents(credit - debit)
        else:
            amount = parse_amount_cents(raw[self.amount_column])
            if self.amount_mode == "outflow_positive":
                amount = validate_cents(-amount)
        return {
            "posted_date": posted_date,
            "description": raw[self.description_column].strip(),
            "account": raw[self.account_column].strip() if self.account_column else self.fixed_account.strip(),
            "source_id": (raw[self.transaction_id_column].strip() or None) if self.transaction_id_column else None,
            "amount_cents": amount,
        }

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)


CANONICAL_MAPPING = ColumnMapping(
    date_column="date", description_column="description", amount_mode="inflow_positive",
    account_column="account", transaction_id_column="transaction_id", amount_column="amount",
)
