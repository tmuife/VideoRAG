class AsyncStatus:
    _instance = None
    _loop_id = 10  # 静态变量

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AsyncStatus, cls).__new__(cls)
        return cls._instance
    def set_id(self, loop_id:str):
        self._loop_id = loop_id
    def get_id(self):
        return self._loop_id
