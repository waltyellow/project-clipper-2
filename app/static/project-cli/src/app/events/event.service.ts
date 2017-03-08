import { Injectable }    from '@angular/core';
import { Http, Response } from '@angular/http';
import {Observable} from 'rxjs/Rx';
import { Event }           from './event';

@Injectable()
export class EventService {
    constructor(private http: Http) { }

    private baseURL = 'http://localhost:5000/events/';

   public getEvents() : Observable<Event[]> {
       return this.http.get(this.baseURL).map((res:Response) => res.json())
    }

    public getEvent(id) : Observable<Event[]> {
       return this.http.get(this.baseURL/id/event).map((res:Response) => res.json())
    }
}