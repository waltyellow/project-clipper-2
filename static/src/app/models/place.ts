export class Place {
    constructor(
        public place_id: string,
        public name: string,
        public rating_count: number,
        public rating_average: number,
        public senti_score: number,
        public geo_coordinates: string,
        public dynamic_senti_score: number
        ){}
}
