class ValidationError(Exception):
    pass


class GenderValidationError(ValidationError):
    pass


class BirthdayValidationError(ValidationError):
    pass


class MailValidationError(ValidationError):
    pass


class UserPassValidationError(ValidationError):
    pass


class DietValidationError(ValidationError):
    pass

class USDAConnectionError(Exception):
    pass
