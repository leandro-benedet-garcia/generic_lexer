import { ProgrammingBody } from "./ast/index";
import { Keyword } from "./ast/programming-body";


export default class Parser {
    programmingBody: ProgrammingBody = ProgrammingBody.instance;

    ignoreWhitespace: boolean = true;
    expectedSymbol: string = ":";
    currBody: string = "";

    /** @TJS-type integer */
    filePointer: number;

    currTrigger: Function = function (parseObject: Parser): void {
        let keyResult: Keyword = this.programmingBody.getKeyword(parseObject.currBody);
        this.currTrigger = keyResult.action;
    };

    constructor(inputValue: string) {
        for (this.filePointer = 0; this.filePointer < inputValue.length; this.filePointer++) {
            const currChar = inputValue[this.filePointer];

            if (this.ignoreWhitespace && this.getDefaultRegex("whiteSpace").test(currChar)) {
                continue;
            }

            if (currChar == this.expectedSymbol) {
                console.log(`The current body is: ${this.currBody}`);
                console.log(`The triggered result is: ${this.currTrigger(this)}`);
                this.currBody = "";
            }

            this.currBody += currChar;
        }
    }

    public getDefaultRegex(regexName: string): RegExp {
        return this.programmingBody.defaultRegex[regexName];
    }

    public testRegex(regexName: string, testValue: string) {
        return this.getDefaultRegex(regexName).test(testValue);
    }
}
