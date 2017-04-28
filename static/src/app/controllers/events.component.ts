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
  public sortOptionsVisible: boolean = false;

  constructor(private titleService: TitleService, private eventService: EventService, private sortService: SortService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.titleService.setTitle('Events');
    this.eventService.getEvents().subscribe(events => this.events = events['events']);

    this.sub = this.route.queryParams.subscribe(params => {
        let sanitizedSearch = params['search']
        this.eventService.getEvents(sanitizedSearch).subscribe(events => {
            this.events = events['events']
            this.sortEventsByDate()
        });
    });
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }

  public sortEventsByName() {
      this.sortService.propertySort<Eventx>(this.events, 'name');
  }

  public sortEventsByProximity() {
      if (!!navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(position => {
              this.events.sort((a, b) => {
                  let d_a = this.distance(a, position)
                  let d_b = this.distance(b, position)
                  if (d_a < d_b) {
                      return -1;
                  } else if (d_a == d_b) {
                      return 0;
                  } else {
                      return 1;
                  }
              });
          });
      }
  }

  distance(event, position) {
      let long1 = event.geo_coordinates.coordinates[0]
      let lat1 = event.geo_coordinates.coordinates[1]
      let long2 = position.coords.longitude
      let lat2 = position.coords.latitude
      return Math.sqrt(Math.pow(long2 - long1, 2) + Math.pow(lat2 - lat1, 2));
  }

  public sortEventsByDate() {
    this.sortService.propertySort<Eventx>(this.events, 'start_time', true);
  }

  setListView(listView: boolean) {
  	 this.listView = listView;
  }

  public toggleDropdown() {
      this.sortOptionsVisible = !this.sortOptionsVisible;
  }
}
