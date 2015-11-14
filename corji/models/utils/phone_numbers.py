def sanitize_phone_number(phone_number):
    return str(phone_number).strip("+").strip()
