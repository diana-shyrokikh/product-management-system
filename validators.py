import re


def validate_string(string, pattern, error_message):
    if string:
        if not re.match(pattern, string.strip()):
            raise ValueError(error_message)

        return string


def validate_number(number, field_name):
    if number:
        if number < 1:
            raise ValueError(
                f"{field_name} must be greater than 0"
            )

        return number


def validate_phone_number_format(phone_number):
    if phone_number:
        phone_number = phone_number.replace(" ", "").replace(
            "(", ""
        ).replace(")", "").replace("+", "").replace("-", "")

        if not phone_number.isdigit():
            raise ValueError(
                "Phone number can contain digits, "
                "spaces, symbols: (, +, -, )"
            )

        return phone_number

