import locale
import unicodedata


def format_currency(price):
    if price is None:
        return "Precio no disponible"
    
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, '')
        except locale.Error:
            return "${:,.2f}".format(price)
    return locale.currency(price, grouping=True)

def normalize_text(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()