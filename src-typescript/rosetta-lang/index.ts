import { default as Parser } from "./parser";

var curr_code = `\
public:Bool is_valid_color(color_code, max_range, min_range? 0: Number)
    ret min_range < color_code < max_range`;

class Main {
    constructor() {
        new Parser(curr_code);
    }
}

new Main();
