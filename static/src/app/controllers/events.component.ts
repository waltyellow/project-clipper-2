import { Component, OnInit } from '@angular/core';   
import {ViewEncapsulation} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { EventService } from '../services/event.service';
import { TitleService } from '../services/title.service';
import { Eventx }        from '../models/eventx';
import { SortService } from '../services/sort.service';


@Component({
  selector: 'app-events',
  templateUrl: '../templates/events.component.html',
})
export class EventsComponent implements OnInit {
  public listView: boolean = true;
  public events: Eventx[];
  
  constructor(private titleService: TitleService, private eventService: EventService, private sortService: SortService) {
  }

  ngOnInit() {
    this.titleService.setTitle('Events');
    this.eventService.getEvents().subscribe(events => this.events = events['events']);
  }

  public sortEvents () {
    this.propertySort.alphabeticSort<Eventx>(this.events, 'name');
  }
  
  setListView(listView: boolean) {
  	 this.listView = listView;
  }
}
