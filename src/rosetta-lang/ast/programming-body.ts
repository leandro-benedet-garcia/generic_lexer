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
                parseObject.expectedSymbol = " ";
        });
    }

    public static get instance(): ProgrammingBody {
        if (!ProgrammingBody._instance) {
            ProgrammingBody._instance = new ProgrammingBody();
        }

        return ProgrammingBody._instance;
    }

    public getKeyword(name: string): Keyword | false {
        let returnedValue: undefined | Keyword = ProgrammingBody.instance.keywords[name];
        if(!returnedValue){
            return false;
        }
        return returnedValue;
    }

    public setKeyword(name: string, scope: Scope, action?: Function): Keyword {
        let created_keyword: Keyword = new Keyword(name, scope, action);

        this.keywords[name] = created_keyword;
        return created_keyword;
    }
}
