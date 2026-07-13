class CrawlerError(Exception):
    """Base class for controlled crawler failures."""


class PolicyDeniedError(CrawlerError):
    """Raised before navigation when a source has not passed every policy gate."""


class ParseError(CrawlerError):
    """Raised when an official-source response cannot be parsed safely."""


class NavigationError(CrawlerError):
    """Raised when Playwright cannot load an approved source."""

