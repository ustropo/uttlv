"""Custom exceptions used along project."""


class ValidationException(Exception):
    """Tag validation has failed."""


class LengthSizeException(Exception):
    """Max length size encode exception."""


class TagSizeException(Exception):
    """Max length for tag encode exception."""


class LengthException(Exception):
    """Data is of wrong length."""
