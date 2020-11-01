import { Scope } from "../enums/index";

export default class Keyword {
    public readonly name: string;
    public readonly scope: Scope;
    public readonly action: Function;

    constructor(name: string, scope: Scope, action?: Function){
        this.name = name;
        this.scope = scope;
        this.action = action;
    }

    public toString(): string{
        return `Keyword name: ${this.name}`;
    }
}
