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

from decimal import Decimal


def calculate_dors_price(

    fabric,
    hood,
    zipper,
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

    # کم شدن کشباف
    body_height -= 5
    sleeve_height -= 5

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
    if body_height < Decimal("0.55"):
        sleeve_factor = Decimal("0.35")
        rib_factor = Decimal("0.40")

    elif body_height < Decimal("0.60"):
        sleeve_factor = Decimal("0.50")
        rib_factor = Decimal("0.30")

    elif body_height < Decimal("0.70"):
        sleeve_factor = Decimal("0.55")
        rib_factor = Decimal("0.25")

    else:
        sleeve_factor = Decimal("0.65")
        rib_factor = Decimal("0.20")

    # قیمت آستین
    sleeve_price = (

        sleeve_height *
        fabric_price *
        (sleeve_factor / fabric_width)

    )

    # قیمت پارچه مصرفی
    fabric_total_price = (
        body_price +
        sleeve_price
    )

    # قیمت کشباف
    rib_price = (
        fabric_total_price *
        rib_factor
    )

    # قیمت کلاه
    hood_price = Decimal("0")

    if hood.name != "بدون کلاه":

        hood_fabric_price = sleeve_price

        hood_price = (

            hood.extra_price +

            hood_fabric_price

        )
        
    # قیمت زیپ
    zipper_price = zipper.extra_price
    
    # قیمت نهایی
    total = (

        fabric_total_price +

        rib_price +

        hood_price +

        zipper_price +

        sticker_price +

        sewing_price

    )

    total = round(total, -3)

    return int(total)

from decimal import Decimal

def calculate_trousers_price(
    fabric,
    leg_model,
    pocket,
    pants_height,
    hip_width,
    sewing_price,
    ):

# --------------------------------
# جا دوخت
# --------------------------------
    pants_height += 3
    hip_width += 3

# --------------------------------
# تبدیل به متر
# --------------------------------
    pants_height = Decimal(str(pants_height)) / Decimal("100")

    hip_width = Decimal(str(hip_width)) / Decimal("100")

# --------------------------------
# اطلاعات پارچه
# --------------------------------
    fabric_price = fabric.price_per_meter

    fabric_width = Decimal(
    str(fabric.fabric_width)
)

# --------------------------------
# قیمت پارچه شلوار
# --------------------------------
    fabric_cost = (

    pants_height *

    fabric_price *

    (hip_width / fabric_width)

    )

# --------------------------------
# جمع کل
# --------------------------------
    total = (

    fabric_cost +

    leg_model.extra_price +

    pocket.extra_price +

    sewing_price

    )


# رند به هزار تومان
    total = round(total, -3)

    return int(total)
