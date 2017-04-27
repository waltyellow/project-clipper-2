export class Comment {
    constructor(
        public message_id: string,
        public body: string,
        public posted: number,
        public username: string,
        public parent: string,
        public type: string,
        public senti_score: number
        ){}
}
