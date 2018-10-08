def _is_multiple_of_six(number):
    """
    Function utility used to check if a number is multiple of six
    :param number:
    :return:
    """
    return (number % 6) == 0


def _is_multiple_of_seven(number):
    """
    Function utility used to check if a number is multiple of seven
    :param number:
    :return:
    """
    return (number % 7) == 0


def multiples(start, end):
    """ Generator used to find multiples of 6 and 7."""
    counter = start
    while counter != end:
        counter += 1
        if _is_multiple_of_seven(counter) and _is_multiple_of_six(counter):
            yield 'Docket Alarm'
        elif _is_multiple_of_seven(counter):
            yield 'Docket'
        elif _is_multiple_of_six(counter):
            yield 'Alarm'
        else:
            yield counter


if __name__ == '__main__':
    for i in multiples(0, 1000):
        print(i)
