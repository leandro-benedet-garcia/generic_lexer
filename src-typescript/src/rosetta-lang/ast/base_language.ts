export type Access = "public"
    | "private"
    | "protected";


export class RosettaBase {
    name: string;
    ownerBody: RosettaIterator<RosettaBase>;
}


export class RosettaIterator<T> extends Array<T> {
    last(): T {
        return this[this.length - 1];
    }
}


export interface IRosettaAccess extends RosettaBase {
    access: Access;
}


export interface IRosettaClass extends IRosettaAccess, RosettaIterator<RosettaBase> {
    meta: boolean;

    constructor: IRosettaFunction;
    childDeclaration: IRosettaFunction;
    beforeChildConstructor: IRosettaFunction;
}


export interface IRosettaFunction extends IRosettaAccess, RosettaIterator<RosettaBase> {
    attributes?: IRosettaVariable[];
}


export interface IRosettaVariable extends IRosettaAccess {
    rosettaType: RosettaBase;
    value?: RosettaBase;
}
