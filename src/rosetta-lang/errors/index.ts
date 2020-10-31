class RosettaError {
    message: string;

    constructor(message: string) {
        this.message = message;
    }
}


class ObjectNotUnique extends RosettaError { }

export { RosettaError, ObjectNotUnique }
