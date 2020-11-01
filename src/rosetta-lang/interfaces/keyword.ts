import { Scope } from "../enums/index";

export default interface Keyword {
    readonly name: string;
    readonly scope: Scope;
    readonly action?: Function;
}
