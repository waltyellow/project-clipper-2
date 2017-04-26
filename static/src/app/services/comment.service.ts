import { Injectable }      from '@angular/core';
import { Http, Response, Headers, RequestOptions }  from '@angular/http';
import {Observable}        from 'rxjs/Rx';
import { Comment }         from '../models/comment';

@Injectable()
export class CommentService {
    constructor(private http: Http) { }
    
    private messageURL = 'http://localhost:5000/messages?parent=';
    private createMessageURL = 'http://localhost:5000/messages/create';

    public getComments(id) : Observable<Comment[]> {
        return this.http.get(this.messageURL + id).map((res:Response) => res.json())
    }

    public postComment(comment) : Observable<Comment> {
        let headers = new Headers({ 'Content-Type': 'application/json' });
        let options = new RequestOptions({ headers: headers });
        
        return this.http.post(this.createMessageURL, comment, options)
            .map((res:Response) => res.json())
    }
}