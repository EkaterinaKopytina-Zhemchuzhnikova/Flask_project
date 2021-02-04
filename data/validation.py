def validation_user_snils(user_snils):
    processed_snils = user_snils.split()
    if ''.join(processed_snils).isdigit() and len(''.join(processed_snils)) == 11:
        return ''.join(processed_snils)
    return None


def validation_user_fio(user_fio):
    processed_fio = user_fio.split()
    if ''.join(processed_fio).isalpha() and len(processed_fio) >= 3:
        return ' '.join(processed_fio)
    return None


def validation_user_phone(user_phone):
    import re

    remainder = ''
    if user_phone.startswith('+7'):
        remainder = user_phone[2:]
    elif user_phone.startswith('8'):
        remainder = user_phone[1:]
    else:
        return False
    remainder = re.sub(r'[ -]', '', remainder)
    if re.match(r'^\(\d{3}\)', remainder):
        remainder = re.sub(r'\(', '', remainder, 1)
        remainder = re.sub(r'\)', '', remainder, 1)
    return bool(re.match(r'^\d{10}$', remainder))
