SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS = True
SITEMAP_URL_SCHEME = 'https'

try:
    from .local import *
except ImportError:
    pass
