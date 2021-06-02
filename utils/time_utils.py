import arrow


def expired(date):
    """ Return True if date string is expired """

    print(date)
    print(type(date))
    n = arrow.utcnow()
    expected = arrow.get(date, "D/M/YYYY")

    return n > expected


