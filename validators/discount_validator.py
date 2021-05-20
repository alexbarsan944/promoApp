from datetime import datetime


def validate(discount):
    ok = True
    ok = ok and validate_percentage(discount.procent)
    ok = ok and validate_date(discount.data_expirare)

    return ok


def validate_percentage(procent):
    return 0 < int(procent) < 100


def validate_date(date_string):
    format = "%d/%m/%Y"
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False


