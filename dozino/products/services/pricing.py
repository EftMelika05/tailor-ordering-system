from decimal import Decimal


def calculate_tshirt_price(
    fabric,
    collar,
    sticker_price,
    body_height,
    body_width,
    sleeve_height,
    sewing_price,
    ):

    # جای دوخت
    body_height += 3
    body_width += 3
    sleeve_height += 3

    # تبدیل به متر
    body_height = Decimal(str(body_height)) / Decimal("100")
    body_width = Decimal(str(body_width)) / Decimal("100")
    sleeve_height = Decimal(str(sleeve_height)) / Decimal("100")

    fabric_price = fabric.price_per_meter
    fabric_width = Decimal(str(fabric.fabric_width))

    # قیمت تنه
    body_price = (
        body_height *
        fabric_price *
        (body_width / fabric_width)
    )

    # ضریب آستین
    if body_height < 0.55:
        sleeve_factor = Decimal(0.35)

    elif body_height < 0.60:
        sleeve_factor = Decimal(0.50)

    elif body_height < 0.70:
        sleeve_factor = Decimal(0.55)

    else:
        sleeve_factor = Decimal(0.65)

    # قیمت آستین
    sleeve_price = (
        sleeve_height *
        fabric_price *
        (sleeve_factor / fabric_width)
    )

    total = (
        body_price +
        sleeve_price +
        collar.extra_price +
        sticker_price +
        sewing_price
    )
    total = round(total, -3)
    return int(total)