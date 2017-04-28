import { Component, Input } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { SortService } from '../services/sort.service';
import { Eventx }        from '../models/eventx';

@Component({
  selector: 'sort',
  templateUrl: '../templates/sort.component.html',
})

export class SortComponent {
 
 constructor(private sortService: SortService) {
  }
  @Input() items: Eventx[];
  @Input() soonest: boolean;

  public sortOptionsVisible: boolean = false;

    public sortEventsByProximity() {
        if (!!navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(position => {
                this.items.sort((a, b) => {
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
        SortService.propertySort<Eventx>(this.items, 'start_time', true);
    }

    public static sortEventsByName(items) {
      SortService.propertySort<Eventx>(items, 'name');
    }

    public sortPlacesByRating() {
        SortService.propertySort(this.items, 'rating_average', true)
    }

    public toggleDropdown() {
        this.sortOptionsVisible = !this.sortOptionsVisible;
    }
}

