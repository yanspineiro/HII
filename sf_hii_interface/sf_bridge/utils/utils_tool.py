import re


def format_phone(old_phone):
    phone = re.sub(r'\D', '', old_phone)
    phone = phone.lstrip('1')
    return '{}-{}-{}'.format(phone[0:3], phone[3:6], phone[6:])

