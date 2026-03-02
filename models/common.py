def to_camel_case(value: str) -> str:
    """
    Convert snake_case string to camelCase.

    Handles:
    - leading/trailing underscores
    - multiple underscores
    - already camelCase input
    """

    if not value:
        return value

    # Убираем лишние подчёркивания по краям
    value = value.strip('_')

    if '_' not in value:
        return value  # уже camelCase или одно слово

    parts = [p for p in value.split('_') if p]

    first = parts[0].lower()
    rest = ''.join(word.capitalize() for word in parts[1:])

    return first + rest
