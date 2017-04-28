import { Injectable }      from '@angular/core';
import { Http, Response, Headers, RequestOptions }  from '@angular/http';
import {Observable}        from 'rxjs/Rx';
import { Place }          from '../models/place';

@Injectable()
export class PlaceService {
    constructor(private http: Http) { }

    private baseURL = 'http://localhost:5000/places/';
    private searchURL = this.baseURL + 'search'

    private getPlaces(type:string, search:string = '') : Observable<Place[]> {
       let url = this.searchURL + '?type=' + type
       if (search) {
           url += '?name_search=' + search
       }
       return this.http.get(url).map((res:Response) => res.json())
    }

    public getPlace(id) : Observable<Place> {
       return this.http.get(this.baseURL + id).map(res => res.json())
    }

    public getBuildings(search:string = '') : Observable<Place[]> {
        return this.getPlaces('CampusBuilding', search)
    }

    public getStudySpaces(search:string = '') : Observable<Place[]> {
        return this.getPlaces('StudyLocation', search)
    }

    public getFoodAndEntertainment(search:string = '') : Observable<Place[]> {
        return this.getPlaces('FoodEntertainment', search)
    }
}
