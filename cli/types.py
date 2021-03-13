import re

import click


class URLParamType(click.types.StringParamType):
    name = 'url'

    VALIDATOR = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )

    def convert(self, value, param, ctx):
        value = super().convert(value, param, ctx)

        if re.match(self.VALIDATOR, value) is None:
            self.fail(
                "'%s' is not a valid URL" % (value,),
                param,
                ctx,
            )

        return value

    def __repr__(self):
        return 'URL'


URL = URLParamType()
