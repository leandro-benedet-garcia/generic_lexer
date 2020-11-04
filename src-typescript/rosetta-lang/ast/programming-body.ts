import { default as Parser } from "../parser";

type ValidJSON = string | number | boolean;

class Node {
    attrs: Map<string, ValidJSON>;
    body: Node[];

    public readonly name: string;

    constructor(name: string, attrs?) {
        this.name = name;
        this.pushAttr(...attrs);
    }

    get last(): Node {
        return this.body[this.body.length - 1];
    }

    pushAttr(...attrs){
        if (!this.attrs) {
            this.attrs = new Map<string, ValidJSON>();
        }


    }

    push(...toAdd: Node[]): number {
        if (!this.body) {
            this.body = [];
        }

        return this.body.push(...toAdd);
    }

    createChild(name: string): Node {
        let createdContext = new Node(name);
        this.push(createdContext);

        return createdContext;
    }

    createInnerChild(name: string): Node {
        return this.last.createChild(name);
    }
}


export class Keyword extends Node {
    public toString(): string {
        return `Keyword name: ${this.name}`;
    }
}


export class ProgrammingBody {
    private static _instance: ProgrammingBody;

    private keywords = new Map<string, Keyword>();
    private defaultType = new Map<string, any>();

    public context = new Node("rosetta");
    public defaultRegex = new Map<string, RegExp>();

    private constructor() {
        this.defaultRegex["typing"] = /[A-B][\w\d]+/;
        this.defaultRegex["commonVariable"] = /[a-z_][a-z\d]+/;
        this.defaultRegex["whiteSpace"] = /\n\t /;
        this.defaultRegex["typePrefix"] = /:/;

        this.defaultType.set("Bool", Boolean);

        this.setKeyword("public", false, function (parseObject: Parser) {
            parseObject.expectedSymbol = " ";
            parseObject.currTrigger = function (parseObject: Parser) {
                parseObject.currBody
            }
        });
    }

    public static get instance(): ProgrammingBody {
        if (!ProgrammingBody._instance) {
            ProgrammingBody._instance = new ProgrammingBody();
        }

        return ProgrammingBody._instance;
    }

    public get localContext() {
        return this.context.last();
    }

    public getType(typeName: string): any {
        if (typeName in this.localContext) {
            return this.localContext[typeName];
        }
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
