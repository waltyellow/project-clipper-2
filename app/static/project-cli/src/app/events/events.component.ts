import { Component, OnInit } from '@angular/core';   
import {ViewEncapsulation} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { EventService } from './event.service'
import { Event }        from './event';


@Component({
  selector: 'app-events',
  templateUrl: './events.component.html',
})
export class EventsComponent implements OnInit {
  public events: Event[];
  constructor(private eventService: EventService) {
  }

  ngOnInit() {
    this.eventService.getEvents().subscribe(events => this.events = events['events'])
  }
}
