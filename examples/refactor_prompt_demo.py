"""Small presentation demo: vague refactor prompt vs. better prompt.

Run:
    python examples/refactor_prompt_demo.py

Presentation flow:
1. Show `total_messy`.
2. Ask AI: "Refactor this function." Show `total_meh_result`.
3. Improve the prompt. Show `total_good_result`.

The point is not that AI magically becomes perfect. The point is that a better
prompt names the job: preserve behavior, expose rules, avoid over-design, and
give yourself a safety check.
"""

from __future__ import annotations

from typing import Any

TAX_RATE = 0.16
BASE_SHIPPING = 5.00
HEAVY_SURCHARGE = 4.00

SAMPLE_ORDER = {
    "customer_tier": "vip",
    "coupon": "WELCOME10",
    "items": [
        {"sku": "BOOK", "kind": "merch", "price": 30.00, "qty": 2, "heavy": False},
        {"sku": "MUG", "kind": "merch", "price": 15.00, "qty": 4, "heavy": True},
        {"sku": "GIFT", "kind": "gift_card", "price": 25.00, "qty": 1, "heavy": False},
    ],
}

VAGUE_PROMPT = "Refactor this function."

BETTER_PROMPT = """
Refactor this function without changing behavior.
Constraints:
- keep one public function that accepts the same order dictionary
- extract helpers only when they reveal a business rule
- name the rules clearly: gift cards, volume discount, coupon, shipping, tax
- keep it small enough for a workshop slide
- add a tiny assertion that proves the refactor preserved the sample result
"""


def total_messy(o: dict[str, Any]) -> float:
    a = 0.0
    b = 0.0
    c = 0.0
    d = BASE_SHIPPING

    for x in o["items"]:
        q = x.get("qty", 1)
        line = x["price"] * q
        if x["kind"] == "gift_card":
            b += line
        else:
            a += line
            if q >= 3:
                c += line * 0.05
            if x.get("heavy") and o.get("customer_tier") != "vip":
                d += HEAVY_SURCHARGE

    if o.get("coupon") == "WELCOME10":
        c += (a - c) * 0.10
    if o.get("customer_tier") == "vip" and a >= 75:
        d = 0.0

    return round(a + b - c + ((a - c) * TAX_RATE) + d, 2)


def total_meh_result(order: dict[str, Any]) -> float:
    """Typical meh result from a vague prompt: nicer names, same tangle."""
    merchandise_total = 0.0
    gift_card_total = 0.0
    discount = 0.0
    shipping = BASE_SHIPPING

    for item in order["items"]:
        quantity = item.get("qty", 1)
        item_total = item["price"] * quantity
        if item["kind"] == "gift_card":
            gift_card_total += item_total
        else:
            merchandise_total += item_total
            if quantity >= 3:
                discount += item_total * 0.05
            if item.get("heavy") and order.get("customer_tier") != "vip":
                shipping += HEAVY_SURCHARGE

    if order.get("coupon") == "WELCOME10":
        discount += (merchandise_total - discount) * 0.10
    if order.get("customer_tier") == "vip" and merchandise_total >= 75:
        shipping = 0.0

    tax = (merchandise_total - discount) * TAX_RATE
    return round(merchandise_total + gift_card_total - discount + tax + shipping, 2)


def total_good_result(order: dict[str, Any]) -> float:
    """Better result: still small, but each helper names a rule."""

    def line_total(item: dict[str, Any]) -> float:
        return item["price"] * item.get("qty", 1)

    def is_gift_card(item: dict[str, Any]) -> bool:
        return item["kind"] == "gift_card"

    def volume_discount(item: dict[str, Any]) -> float:
        if is_gift_card(item) or item.get("qty", 1) < 3:
            return 0.0
        return line_total(item) * 0.05

    merch_items = [item for item in order["items"] if not is_gift_card(item)]
    gift_card_total = sum(line_total(item) for item in order["items"] if is_gift_card(item))
    merchandise_total = sum(line_total(item) for item in merch_items)

    discount = sum(volume_discount(item) for item in merch_items)
    if order.get("coupon") == "WELCOME10":
        discount += (merchandise_total - discount) * 0.10

    shipping = BASE_SHIPPING
    if order.get("customer_tier") == "vip" and merchandise_total >= 75:
        shipping = 0.0
    elif any(item.get("heavy") for item in merch_items):
        shipping += HEAVY_SURCHARGE

    tax = (merchandise_total - discount) * TAX_RATE
    return round(merchandise_total + gift_card_total - discount + tax + shipping, 2)


if __name__ == "__main__":
    messy = total_messy(SAMPLE_ORDER)
    meh = total_meh_result(SAMPLE_ORDER)
    good = total_good_result(SAMPLE_ORDER)

    assert messy == meh == good

    print("Vague prompt:")
    print(VAGUE_PROMPT)
    print()
    print("Better prompt:")
    print(BETTER_PROMPT.strip())
    print()
    print(f"All versions preserve the sample result: {good}")
