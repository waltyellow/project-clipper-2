import { Injectable }      from '@angular/core';
import { Http, Response, Headers, RequestOptions }  from '@angular/http';
import {Observable}        from 'rxjs/Rx';
import { Building }          from '../models/building';

@Injectable()
export class BuildingsService {
  constructor(private http: Http) { }

  private baseURL = 'http://localhost:5000/buildings/';

  public getBuildings() : Observable<Building[]>{
    return this.http.get(this.baseURL).map((res:Response) => res.json())
  }

  public getBuilding(id) : Observable<Building> {
    return this.http.get(this.baseURL + id).map(res =>res.json())
  }
}
