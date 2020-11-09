class MiniEnum:
    def __new__(cls, *args):
        for curr_index, curr_arg in enumerate(args):
            setattr(cls, curr_arg, curr_index ** 2)
