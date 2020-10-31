import { default as Parser } from "./parser";


class Main {
    constructor() {
        let curr_code = `public:Bool is_valid_color(color_code, max_range, min_range? 0: Number)
        ret min_range < color_code < max_range`;

        let out: Parser = new Parser(curr_code);

        let code_element: HTMLDivElement = document.createElement("div");
        code_element.id = "";
        code_element.innerHTML = curr_code;

        document.body.appendChild(code_element);
    }
}

new Main();
