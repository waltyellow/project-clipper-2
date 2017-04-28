import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { TitleService } from '../services/title.service';
import { PlaceService } from '../services/place.service';
import { Place }        from '../models/place';
import { ActivatedRoute } from '@angular/router';
import { SortComponent } from './sort.component';


@Component({
  selector: 'app-buildings',
  templateUrl: '../templates/buildings.component.html',
  styles: []
})
export class BuildingsComponent implements OnInit {
  public buildings: Place[];
  public sub: any;
  public searchText: string = "";

  constructor(private titleService: TitleService, private placeService: PlaceService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.titleService.setTitle('Campus Buildings');

    this.sub = this.route.queryParams.subscribe(params => {
        let sanitizedSearch = params['search']
        this.placeService.getBuildings(sanitizedSearch).subscribe(buildings => {
            this.buildings = buildings['places']
            SortComponent.sortByRating(this.buildings);
        });
    });
  }
}
