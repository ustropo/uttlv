class ValidationException(Exception):
    """Tag validation has failed."""

    pass


class LengthSizeException(Exception):
    """Max length size encode exception."""

    pass


class TagSizeException(Exception):
    """Max length for tag encode exception."""

    pass


class LengthException(Exception):
    """Data is of wrong length."""

    pass
