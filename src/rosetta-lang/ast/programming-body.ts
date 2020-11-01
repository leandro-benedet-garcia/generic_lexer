import { default as Parser } from "../parser";



class Action {
    public readonly name: string;
    public readonly action: Function;
    public readonly body: any[];

    constructor(name: string, action?: Function, hasBody?: true) {
        this.name = name;
        this.action = action;
        if (hasBody) {
            this.body = new Array<any>();
        }
    }
}


export class Keyword extends Action {
    public toString(): string {
        return `Keyword name: ${this.name}`;
    }
}


export class ProgrammingBody {
    private static _instance: ProgrammingBody;

    private keywords = new Map<string, Keyword>();
    private defaultType = new Map<string, any>();

    public contexts = new Map<string, Action[]>()
    public defaultRegex = new Map<string, RegExp>();

    private constructor() {
        this.defaultRegex["typing"] = /[A-B][\w\d]+/;
        this.defaultRegex["commonVariable"] = /[a-z_][a-z\d]+/;
        this.defaultRegex["whiteSpace"] = /\n\t /;
        this.defaultRegex["typePrefix"] = /:/;

        this.defaultType.set("Bool", Boolean);

        this.setKeyword("public", false, function (parseObject: Parser) {
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
        let returnedValue: Keyword = ProgrammingBody.instance.keywords[name];
        if (!returnedValue) {
            return false;
        }
        return returnedValue;
    }

    public setKeyword(name: string, ...attrs: any[]): Keyword {
        let created_keyword: Keyword = new Keyword(name, ...attrs);

        this.keywords[name] = created_keyword;
        return created_keyword;
    }
}
