import { Component } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { TitleService } from './services/title.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class AppComponent {
    public title: string;

    constructor(titleService: TitleService) {
        titleService.title.subscribe((title) => {
            this.title = title;
        });
    }
}
