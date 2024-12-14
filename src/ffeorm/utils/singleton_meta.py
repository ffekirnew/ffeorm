from threading import Lock


class SingletonMeta(type):
    """
    A thread-safe implementation of Singleton metaclass.

    This metaclass ensures that only one instance of a class is created and provides a global point of access to that instance.

    Attributes:
        _instances (dict): A dictionary to hold the single instance of each class.
        _lock (Lock): A lock object to ensure thread-safe instantiation of the singleton.
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Controls the instantiation of the singleton instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            object: The single instance of the class.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
