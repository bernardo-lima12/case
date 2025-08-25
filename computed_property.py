class computed_property:
    def __init__(self, *args):
        self.args = args
        self.func = None

    def __call__(self, func):
        self.func = func
        self.__doc__ = func.__doc__
        return self

    # main caching logic
    def __get__(self, obj, objtype):
        if obj is None:
            return self

        # criando essa variável por redability (poderiamos so fazer o check
        # hasattr(obj, args_id))
        cache_id = f'_{self.func.__name__}_cache'
        args_id = f'_{self.func.__name__}_args'

        func_args = self._get_current_args(obj)

        if hasattr(obj, cache_id) and getattr(obj, args_id) == func_args:
            print(f"returning cached results for {self.func.__name__}")
            return getattr(obj, cache_id)

        print(f"computing value for {self.func.__name__}")
        value = self.func(obj)

        setattr(obj, cache_id, value)
        setattr(obj, args_id, func_args)

        return value

    def __set__(self, obj, value):
        if self._setter is None:
            raise AttributeError(f"can't set attribute '{self.func.__name__}'")

        self._setter(obj, value)
        cache_id = f'_{self.func.__name__}_cache'
        if hasattr(obj, cache_id):
            delattr(obj, cache_id)

    def __delete__(self, obj):
        if self._deleter is None:
            raise AttributeError(f"can't delete attribute '{self.func.__name__}'")

        self._deleter(obj)
        cache_id = f'_{self.func.__name__}_cache'
        if hasattr(obj, cache_id):
            delattr(obj, cache_id)

    def setter(self, func):
        self._setter = func
        return self

    def deleter(self, func):
        self._deleter = func
        return self

    def _get_current_args(self, obj):
        """Return the values of the decorator arguments acording to the decorated
        function. If the argument does not exist in the decorated functions, returns
        a sentinel object."""

        return tuple(getattr(obj, arg, object()) for arg in self.args)
