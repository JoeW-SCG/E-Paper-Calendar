class DataSourceInterface (object):
    """Interface for child interfaces that fetch data."""
    def is_available (self):
        raise NotImplementedError("Functions needs to be implemented")

    def reload (self):
        raise NotImplementedError("Functions needs to be implemented")