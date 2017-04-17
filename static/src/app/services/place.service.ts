import { Injectable }      from '@angular/core';
import { Http, Response, Headers, RequestOptions }  from '@angular/http';
import {Observable}        from 'rxjs/Rx';
import { Place }          from '../models/place';

@Injectable()
export class PlaceService {
    constructor(private http: Http) { }

    private baseURL = 'http://localhost:5000/places/';

    public getPlaces() : Observable<Place[]> {
       return this.http.get(this.baseURL).map((res:Response) => res.json())
    }

    public getPlace(id) : Observable<Place> {
       return this.http.get(this.baseURL + id).map(res => res.json())
    }
}