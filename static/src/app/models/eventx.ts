export class Eventx {
    constructor(
        public event_id: string,
        public name: string,
        public start_time: number,
        public duration: number,
        public senti_score: number,
        public dynamic_senti_score: number,
        public location: string
        ){}
}
