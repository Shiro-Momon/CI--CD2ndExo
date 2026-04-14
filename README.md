# CI/CD 2nd Exo — FastAPI Delivery & Validation API

A FastAPI project built with TDD, covering a delivery pricing engine, promo codes, surge pricing, and user validation utilities — all wired together via a REST API and tested end-to-end.

## Features

- **Delivery engine** — calculates order totals with distance fees, weight surcharges, promo codes, and surge pricing
- **Validators** — email, password strength, age
- **Utils** — capitalize, slugify, average, clamp, sort students
- **REST API** — order simulation, order creation, promo code validation
- **CI pipeline** — lint + tests + coverage enforced at 80% via GitHub Actions

## Project Structure

```
src/
  delivery.py     # calculateDeliveryFee, applyPromoCode, calculateSurge, calculateOrderTotal
  validators.py   # isValidEmail, isValidPassword, isValidAge
  utils.py        # capitalize, slugify, calculateAverage, clamp, sortStudents
  main.py         # FastAPI app — all routes

tests/
  delivery_test.py  # 45 unit tests
  main_test.py      # 24 integration tests
  validator_test.py
  utils_test.py

.github/workflows/ci.yml  # GitHub Actions CI pipeline
```

## API Routes

### Orders

| Method | Route | Description |
|--------|-------|-------------|
| `POST` | `/orders/simulate` | Calculate price breakdown without saving |
| `POST` | `/orders` | Create and save an order (returns UUID) |
| `GET`  | `/orders/{id}` | Retrieve a saved order by ID |

**Request body (`/orders` and `/orders/simulate`):**
```json
{
  "items": [{ "name": "Pizza", "price": 12.50, "quantity": 2 }],
  "distance": 5,
  "weight": 1,
  "promoCode": "BIENVENUE20",
  "hour": 19.0,
  "dayOfWeek": 1
}
```

**Response:**
```json
{
  "subtotal": 25.00,
  "discount": 5.00,
  "deliveryFee": 4.50,
  "surge": 1.5,
  "total": 24.50
}
```

### Promo codes

| Method | Route | Description |
|--------|-------|-------------|
| `POST` | `/promo/validate` | Check if a promo code is valid for a given amount |

**Request body:**
```json
{ "code": "BIENVENUE20", "amount": 50.0 }
```

### Validators & Utils

| Method | Route | Description |
|--------|-------|-------------|
| `GET`  | `/utils/capitalize?text=hello` | Capitalize a string |
| `GET`  | `/utils/slugify?text=Hello World` | Slugify a string |
| `POST` | `/validators/password` | Validate password strength |
| `POST` | `/validators/profile` | Validate email + age |

## Delivery Pricing Rules

| Condition | Effect |
|-----------|--------|
| Base fee | +2.00€ |
| Distance ≤ 3 km | Included in base |
| Distance 3–10 km | +0.50€/km beyond 3 km |
| Distance > 10 km | Refused (error) |
| Weight > 5 kg | +1.50€ |
| Negative distance or weight | Error |

## Surge Pricing

| Time slot | Multiplier |
|-----------|-----------|
| Mon–Thu 10h–11h30, 14h–18h | ×1.0 |
| Mon–Thu 12h–13h30 | ×1.3 |
| Mon–Thu 19h–22h | ×1.5 |
| Fri–Sat 19h–22h | ×1.8 |
| Sunday all day | ×1.2 |
| Before 10h or from 22h | ×0 (closed) |

## Available Promo Codes

| Code | Type | Value | Min. Order |
|------|------|-------|------------|
| `BIENVENUE20` | percentage | 20% | 15.00€ |
| `FIXED5` | fixed | 5€ | 10.00€ |

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn src.main:app --reload
```

Interactive docs available at `http://localhost:8000/docs`.

## Running Tests

```bash
task test      # run all tests
task coverage  # tests + coverage report
```

Or directly with pytest:

```bash
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

Current coverage: **94%**

## Linting & Formatting

```bash
task lint    # ruff check .
task format  # ruff format .
```

## Available Tasks (taskipy)

| Command | Description |
|---------|-------------|
| `task lint` | Run Ruff linter |
| `task format` | Run Ruff formatter |
| `task test` | Run all tests with pytest |
| `task coverage` | Run tests with coverage report |

## CI Pipeline

GitHub Actions runs on every push and pull request to `main`:

1. Install dependencies
2. Lint with Ruff
3. Run tests with pytest-cov (fails if coverage < 80%)
