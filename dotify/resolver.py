from jsonschema import RefResolver


class RelativePathRefResolver(RefResolver):
    def resolve_remote(self, uri):
        if uri.startswith('file://') and not uri.startswith('file:///'):
            relative_path = uri[len('file://'):]
            return super().resolve_remote(f'file:///{relative_path}')
