# Compass Money Conventions and Golden Test Cases

## Money rules

### Storage
Signed integer cents (`amount_cents`), never float.
floats do not store exact decimals after operations such as +, -, etc; hence integer cents

### Spending
`-(sum of purchase + refund amounts)` in the period, reported as a positive number.

### Refunds
Net against their merchant/category in the period they post. A period can be a "net refund".

### Transfers
Excluded from spending and from net cash flow. Always listed as excluded.
transfers are redundant transactions as money is just circulated among various user accounts
they do not give any cash-in/cash-out insignt

### Income
Excluded from spending. Included in net recorded cash flow.

### Periods
Half-open range `[start, end)` on posted date. A month is a calendar month.

### Currency
Never summed across currencies. One total per currency.
our demo has only USD, hence only one currency in use

### Rounding
Only at display or for ratios, using ROUND_HALF_UP. Percentages show 1 decimal.
ROUND_HALF_UP always rounds away from origin ie 0
eg 2.5 -> 3, -2.5 -> -3

### Empty sets
Average of 0 transactions = None ("no data"), never 0.
to avoid average of $0.00 confusion

## The 10 golden cases

1. Parse "-5.75"
   - Expected: -575

2. Parse "-0.10" + parse "-0.20"
   - Expected: -30
   - Note: float math would give -0.30000000000000004

3. Parse "1.005"
   - Expected: ValueError (more than 2 decimals)

4. October Shopping: T3 -4000, T4 +1500
   - Expected: spending 2500

5. Refund +1500 with no purchase in that period
   - Expected: spending -1500, labeled "net refund $15.00"

6. October fixture including the T5 transfer
   - Expected: spending 3700, with T5 in the excluded list

7. October net recorded cash flow
   - Expected: 196300
   - Note: 200000 income - 3700 spending; transfer excluded

8. Period Oct 1 to Nov 1, with one transaction on Nov 1 and T7 on Nov 4
   - Expected: both Nov 1 and Nov 4 excluded (end date is exclusive)

9. USD -1000 and EUR -500
   - Expected: two totals {USD: 1000, EUR: 500} plus a mixed-currency warning

10. Average of 0 transactions, and pct_change(0, 3000)
    - Expected: None and None