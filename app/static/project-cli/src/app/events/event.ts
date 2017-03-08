export class Event {
    constructor(
        public eventId: integer,
        public name: string,
        public start_time: Time,
        public duration: integer,
        public senti_score: integer,
        public location: string
        ){}
}
