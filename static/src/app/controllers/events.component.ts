import { Component, OnInit } from '@angular/core';   
import {ViewEncapsulation} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { EventService } from '../services/event.service'
import { Eventx }        from '../models/eventx';


@Component({
  selector: 'app-events',
  templateUrl: '../templates/events.component.html',
})
export class EventsComponent implements OnInit {
  public events: Eventx[];
  constructor(private eventService: EventService) {
  }

  ngOnInit() {
    this.eventService.getEvents().subscribe(events => this.events = events['events'])
  }
}
