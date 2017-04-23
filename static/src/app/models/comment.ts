export class Comment {
    constructor(
        public message_id: string,
        public message_body: string,
        public message_timestamp: number,
        public message_username: string,
        public message_parent: string,
        ){}
}
