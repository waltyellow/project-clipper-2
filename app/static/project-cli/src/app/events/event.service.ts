import { Injectable }    from '@angular/core';
import { Http, Response } from '@angular/http';
import {Observable} from 'rxjs/Rx';
import { Eventx }          from './eventx';

@Injectable()
export class EventService {
    constructor(private http: Http) { }

    private baseURL = 'http://localhost:5000/events/';

   public getEvents() : Observable<Eventx[]> {
       return this.http.get(this.baseURL).map((res:Response) => res.json())
    }

    public getEvent(id) : Observable<Eventx> {
       return this.http.get(this.baseURL + id).map(res => res.json())
        //.map(response => <string[]> response.json().petfinder.pet);
    }
}