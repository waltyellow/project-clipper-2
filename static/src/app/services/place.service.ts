import { Injectable }      from '@angular/core';
import { Http, Response, Headers, RequestOptions }  from '@angular/http';
import {Observable}        from 'rxjs/Rx';
import { Placex }          from '../models/placex';

@Injectable()
export class PlaceService {
    constructor(private http: Http) { }

    private baseURL = 'http://localhost:5000/places/';

    public getPlaces() : Observable<Placex[]> {
       return this.http.get(this.baseURL).map((res:Response) => res.json())
    }

    public getPlace(id) : Observable<Placex> {
       return this.http.get(this.baseURL + id).map(res => res.json())
    }
}