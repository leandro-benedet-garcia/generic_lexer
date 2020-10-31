import { ProgrammingBody } from "./ast/index";


enum Action {
    Create,
    Read,
    Set,
    Delete
}


enum ScopeType {
    Module,
    Namespace,
    Class,
    Function
}


interface Scope {
    name: string;
    content: string;
    scopeType: ScopeType;
}


export default class Parser {
    allScopes: Scope[];

    programmingBody: ProgrammingBody = ProgrammingBody.instance;

    ignoreWhitespace: boolean = true;
    expectedSymbol: string = ":";
    currBody: string = "";
    filePointer: number = -1;
    whatToFind: RegExp = this.getDefaultRegex("typePrefix");

    currTrigger: Function = this.programmingBody.getKeyword;

    constructor(inputValue: string) {
        for (let currChar of inputValue) {
            this.filePointer += 1;

            if (this.ignoreWhitespace && this.getDefaultRegex("whiteSpace").test(currChar)) {
                continue;
            }

            if (this.whatToFind.test(currChar)) {
                let triggered = this.currTrigger(this.currBody);
                if(triggered){

                }

                this.currBody = "";
            } else if (
                !this.testRegex("typing", currChar) &&
                !this.testRegex("commonVariable", currChar)
            ) {
                throw `Syntax error char ${currChar} not expected`;
            }

            this.currBody += currChar;
        }
    }

    public getDefaultRegex(regexName: string): RegExp{
        return this.programmingBody.defaultRegex[regexName];
    }

    public testRegex(regexName: string, testValue: string){
        return this.getDefaultRegex(regexName).test(testValue);
    }
}
