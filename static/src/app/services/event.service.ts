import { Injectable }      from '@angular/core';
import { Http, Response, Headers, RequestOptions }  from '@angular/http';
import {Observable}        from 'rxjs/Rx';
import { Eventx }          from '../models/eventx';

@Injectable()
export class EventService {
    constructor(private http: Http) { }

    private baseURL = 'http://localhost:5000/events/';

    public getEvents(search: string = '') : Observable<Eventx[]> {
        let url = this.baseURL
        if (search) {
            url += 'search?name_search=' + search
        }
        return this.http.get(url).map((res:Response) => res.json())
    }

    public getEvent(id) : Observable<Eventx> {
       return this.http.get(this.baseURL + id).map(res => res.json())
    }
}
