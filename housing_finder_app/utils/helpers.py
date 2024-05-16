import locale


def format_currency(price):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Set locale to use proper currency formatting
    return locale.currency(price, grouping=True)