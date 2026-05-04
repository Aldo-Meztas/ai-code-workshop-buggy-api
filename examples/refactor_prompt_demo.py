"""Presentation demo: vague refactor prompt vs. better prompt.

Run:
    python examples/refactor_prompt_demo.py

Presentation flow:
1. Show `summarize_cart`.
2. Ask AI: "Refactor this function." Show `summarize_cart_meh_result`.
3. Improve the prompt. Show `summarize_cart_good_result`.

Lesson: a vague prompt can make code prettier while preserving the bugs.
"""

VAGUE_PROMPT = "Refactor this function."

BETTER_PROMPT = """
Refactor this function, but first identify likely business-rule bugs.
Keep the same public signature and return shape.
Fix only these rules:
- SAVE10 discounts the subtotal only, not tax or shipping
- premium free shipping uses subtotal before discount and starts at >= 100
"""

PRODUCTS = {
    "book": (42, True, True, False),
    "usb": (25, True, True, False),
    "keyboard": (100, True, True, True),
    "gift-card": (50, False, False, False),
}


def summarize_cart(cart, user, coupon=None):
    total = 0
    tax = 0
    shipping = 5
    warnings = []

    for item in cart:
        sku = item.get("sku")
        qty = item.get("qty", 1)

        if sku == "book":
            price = 42
            taxable = True
            shippable = True
            heavy = False
        elif sku == "usb":
            price = 25
            taxable = True
            shippable = True
            heavy = False
        elif sku == "keyboard":
            price = 100
            taxable = True
            shippable = True
            heavy = True
        elif sku == "gift-card":
            price = 50
            taxable = False
            shippable = False
            heavy = False
        else:
            warnings.append("unknown sku ignored")
            continue

        line = price * qty
        total += line

        if taxable:
            tax += line * 0.16

        if shippable and heavy:
            shipping += 3

    if coupon == "SAVE10":
        # bug: discounts tax and shipping too
        discount = (total + tax + shipping) * 0.10
    else:
        discount = 0

    if user.get("premium") and total - discount > 100:
        # bug: threshold should be before discount and >= 100
        shipping = 0

    final = total + tax + shipping - discount

    return {
        "subtotal": round(total, 2),
        "tax": round(tax, 2),
        "shipping": round(shipping, 2),
        "discount": round(discount, 2),
        "total": round(final, 2),
        "warnings": warnings,
    }


def summarize_cart_meh_result(cart, user, coupon=None):
    """Typical vague-prompt result: tidier lookup, same hidden rule bugs."""
    subtotal = 0
    tax = 0
    shipping = 5
    warnings = []

    for item in cart:
        product = PRODUCTS.get(item.get("sku"))
        if product is None:
            warnings.append("unknown sku ignored")
            continue

        price, taxable, shippable, heavy = product
        line = price * item.get("qty", 1)
        subtotal += line

        if taxable:
            tax += line * 0.16
        if shippable and heavy:
            shipping += 3

    discount = (subtotal + tax + shipping) * 0.10 if coupon == "SAVE10" else 0

    if user.get("premium") and subtotal - discount > 100:
        shipping = 0

    return {
        "subtotal": round(subtotal, 2),
        "tax": round(tax, 2),
        "shipping": round(shipping, 2),
        "discount": round(discount, 2),
        "total": round(subtotal + tax + shipping - discount, 2),
        "warnings": warnings,
    }


def summarize_cart_good_result(cart, user, coupon=None):
    """Better prompt result: same shape, clearer rules, fixed edge cases."""
    subtotal = 0
    tax = 0
    has_heavy_item = False
    warnings = []

    for item in cart:
        product = PRODUCTS.get(item.get("sku"))
        if product is None:
            warnings.append("unknown sku ignored")
            continue

        price, taxable, shippable, heavy = product
        line = price * item.get("qty", 1)
        subtotal += line

        if taxable:
            tax += line * 0.16
        if shippable and heavy:
            has_heavy_item = True

    discount = subtotal * 0.10 if coupon == "SAVE10" else 0
    shipping = 0 if user.get("premium") and subtotal >= 100 else 5
    if shipping and has_heavy_item:
        shipping += 3

    return {
        "subtotal": round(subtotal, 2),
        "tax": round(tax, 2),
        "shipping": round(shipping, 2),
        "discount": round(discount, 2),
        "total": round(subtotal + tax + shipping - discount, 2),
        "warnings": warnings,
    }


NORMAL_CART = [{"sku": "book"}, {"sku": "usb", "qty": 2}, {"sku": "missing"}]
BUG_REVEALING_CART = [{"sku": "keyboard"}]


if __name__ == "__main__":
    normal_user = {"premium": False}
    premium_user = {"premium": True}

    assert summarize_cart(NORMAL_CART, normal_user) == summarize_cart_meh_result(NORMAL_CART, normal_user)
    assert summarize_cart(NORMAL_CART, normal_user) == summarize_cart_good_result(NORMAL_CART, normal_user)

    messy_edge = summarize_cart(BUG_REVEALING_CART, premium_user, coupon="SAVE10")
    meh_edge = summarize_cart_meh_result(BUG_REVEALING_CART, premium_user, coupon="SAVE10")
    good_edge = summarize_cart_good_result(BUG_REVEALING_CART, premium_user, coupon="SAVE10")

    assert messy_edge == meh_edge
    assert good_edge != messy_edge
    assert good_edge["discount"] == 10
    assert good_edge["shipping"] == 0

    print("Vague prompt:")
    print(VAGUE_PROMPT)
    print()
    print("Better prompt:")
    print(BETTER_PROMPT.strip())
    print()
    print("Bug-revealing input:")
    print(BUG_REVEALING_CART, premium_user, "coupon=SAVE10")
    print()
    print("Messy / meh result:")
    print(messy_edge)
    print()
    print("Better-prompt result:")
    print(good_edge)
