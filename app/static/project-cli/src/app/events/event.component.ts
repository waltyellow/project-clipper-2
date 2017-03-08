import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { EventService } from './event.service'

@Component({
  selector: 'app-event',
  templateUrl: './event.component.html',
  styleUrls: ['./event.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class EventComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
