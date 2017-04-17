import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import {TitleService} from '../services/title.service';


@Component({
  selector: 'app-home',
  templateUrl: '../templates/home.component.html',
})
export class HomeComponent implements OnInit {
  constructor(private titleService: TitleService) { }

  ngOnInit() {
    this.titleService.useDefaultTitle();
  }
}
