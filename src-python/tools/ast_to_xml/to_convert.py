def is_valid_color(color_code, min_range, max_range):
    return min_range < color_code < max_range

class ColorBase(type):
    name: str

    def __init_subclass__(cls):
        pass

    def is_valid(self, **kwargs) -> bool:
        raise NotImplementedError
