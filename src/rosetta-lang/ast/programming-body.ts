import { Keyword } from "../interfaces/index";
import { Scope } from "../enums/index";
import { default as Parser} from "../parser";


export default class ProgrammingBody {
    private static _instance: ProgrammingBody;

    private keywords: Map<string, Keyword> = new Map<string, Keyword>();

    defaultRegex: Map<string, RegExp> = new Map<string, RegExp>();

    private constructor() {
        this.defaultRegex["typing"] = /[A-B][\w\d]+/;
        this.defaultRegex["commonVariable"] = /[a-z_][a-z\d]+/;
        this.defaultRegex["whiteSpace"] = /\n\t /;
        this.defaultRegex["typePrefix"] = /:/;

        this.setKeyword("public", Scope.Global, function(parseObject: Parser){
                parseObject.whatToFind = this.defaultRegex.whiteSpace;

                parseObject.currTrigger = function(){

                }
        });
    }

    public static get instance(): ProgrammingBody {
        if (!ProgrammingBody._instance) {
            ProgrammingBody._instance = new ProgrammingBody();
        }

        return ProgrammingBody._instance;
    }

    public getKeyword(name: string): Keyword | boolean {
        let returnedValue: undefined | Keyword = this.keywords.get(name);
        if(!returnedValue){
            return false;
        }
        return returnedValue;
    }

    public setKeyword(name: string, scope: Scope, action?: Function): void {
        this.keywords["name"] = {
            "name": name,
            "scope": scope,
            "action": action
        }
    }
}
