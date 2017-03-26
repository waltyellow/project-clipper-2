import { Injectable }      from '@angular/core';
import { Http, Response, Headers, RequestOptions }  from '@angular/http';
import {Observable}        from 'rxjs/Rx';
import { Eventx }          from '../models/eventx';
import { Comment }         from '../models/comment';

@Injectable()
export class EventService {
    constructor(private http: Http) { }

    private baseURL = 'http://localhost:5000/events/';
    private messageURL = 'http://localhost:5000/messages/parent/';
    private createMessageURL = 'http://localhost:5000/messages/create';

   public getEvents() : Observable<Eventx[]> {
       return this.http.get(this.baseURL).map((res:Response) => res.json())
    }

    public getEvent(id) : Observable<Eventx> {
       return this.http.get(this.baseURL + id).map(res => res.json())
    }

    public getComments(id) : Observable<Comment[]> {
        return this.http.get(this.messageURL + id).map((res:Response) => res.json())
    }

    private getEmptyComment() : Observable<Comment> {
        return this.http.get(this.createMessageURL).map((res:Response) => res.json())
    }

    public postComment(comment) : Observable<Comment> {
        let headers = new Headers({ 'Content-Type': 'application/json' });
        let options = new RequestOptions({ headers: headers });
        let emptyComment = this.getEmptyComment()
        return this.http.post(this.createMessageURL, emptyComment, options)
        .map((res:Response) => res.json())
    }
}