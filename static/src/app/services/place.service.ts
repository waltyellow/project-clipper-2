import { Injectable }      from '@angular/core';
import { Http, Response, Headers, RequestOptions }  from '@angular/http';
import {Observable}        from 'rxjs/Rx';
import { Place }          from '../models/place';

@Injectable()
export class PlaceService {
    constructor(private http: Http) { }

    private baseURL = 'http://localhost:5000/places/';
    private searchURL = this.baseURL + 'search'

    public getPlaces() : Observable<Place[]> {
       return this.http.get(this.baseURL).map((res:Response) => res.json())
    }

    public getPlace(id) : Observable<Place> {
       return this.http.get(this.baseURL + id).map(res => res.json())
    }

    public getBuildings() : Observable<Place[]> {
        return this.http.get(this.searchURL + '?type=CampusBuilding').map(res => res.json())
    }
    public getStudyLocations() : Observable<Place[]> {
        return this.http.get(this.searchURL + '?type=StudyLocation').map(res => res.json())
    }
}