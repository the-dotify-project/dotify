from re import match


def assert_valid_url(regex, url, exception):
    try:
        assert match(regex, url) is not None
    except AssertionError as e:
        raise exception
