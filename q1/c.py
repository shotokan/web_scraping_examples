
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


def find_multiples(n):
    if _is_multiple_of_seven(n) and _is_multiple_of_six(n):
        return 'Docket Alarm'
    elif _is_multiple_of_seven(n):
        return 'Docket'
    elif _is_multiple_of_six(n):
        return 'Alarm'
    else:
        return n


if __name__ == '__main__':
    for n in range(1, 1001):
        print(find_multiples(n))
