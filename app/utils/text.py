def format_number(number: int) -> str:
    if number >= 1000:
        return f"{number:,}".replace(",", ".")
    return str(number)
