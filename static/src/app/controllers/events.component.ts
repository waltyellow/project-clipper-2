import { Component, OnInit } from '@angular/core';   
import {ViewEncapsulation} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { EventService } from '../services/event.service';
import { TitleService } from '../services/title.service';
import { Eventx }        from '../models/eventx';


@Component({
  selector: 'app-events',
  templateUrl: '../templates/events.component.html',
})
export class EventsComponent implements OnInit {
  public events: Eventx[];
  constructor(private titleService: TitleService, private eventService: EventService) {
  }

  ngOnInit() {
    this.titleService.setTitle('Events');
    this.eventService.getEvents().subscribe(events => this.events = events['events'])
  }
}
