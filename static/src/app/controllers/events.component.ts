import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
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
  public sub: any;
  public searchText: string = "";

  constructor(private titleService: TitleService, private eventService: EventService, private sortService: SortService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.titleService.setTitle('Events');

    this.sub = this.route.queryParams.subscribe(params => {
        let sanitizedSearch = params['search']
        this.eventService.getEvents(sanitizedSearch).subscribe(events => {
            this.events = events['events']
        });
    });
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }

  setListView(listView: boolean) {
  	 this.listView = listView;
  }
}
