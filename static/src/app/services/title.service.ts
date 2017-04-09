import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs/Rx';

@Injectable()
export class TitleService {
    private defaultTitle = 'Campus Assistant';
    private _title: BehaviorSubject<string> = new BehaviorSubject(this.defaultTitle);
    public title: Observable<string> = this._title.asObservable();

    constructor() {}

    public setTitle(newTitle: string) {
        this._title.next(newTitle);
    }

    public useDefaultTitle() {
        this._title.next(this.defaultTitle);
    }
}
