import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { PlaceService } from '../services/place.service';
import { TitleService } from '../services/title.service';
import { Place }        from '../models/place';
import { SortService } from '../services/sort.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-events',
  templateUrl: '../templates/entertainments.component.html',
})
export class EntertainmentsComponent implements OnInit {
  public places: Place[];
  public sub: any;
  public searchText: string = "";
  public sortOptionsVisible: boolean = false;

  constructor(private titleService: TitleService, private placeService: PlaceService, private sortService: SortService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.titleService.setTitle('Food & Entertainment');

    this.sub = this.route.queryParams.subscribe(params => {
        let sanitizedSearch = params['search']
        this.placeService.getFoodAndEntertainment(sanitizedSearch).subscribe(places => {
            this.places = places['places']
            this.sortPlacesByRating();
        });
    });
  }

  public toggleDropdown() {
      this.sortOptionsVisible = !this.sortOptionsVisible;
  }

  public sortPlacesByRating() {
      this.sortService.propertySort(this.places, 'rating_average', true)
  }

  public sortPlacesByDistance() {

  }

  public sortPlacesByName() {
      this.sortService.propertySort(this.places, 'name')
  }
}
