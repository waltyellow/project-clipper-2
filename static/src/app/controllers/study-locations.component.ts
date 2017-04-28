import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { TitleService } from '../services/title.service';
import { PlaceService } from '../services/place.service';
import { Place }        from '../models/place';
import { SortService } from '../services/sort.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-study-locations',
  templateUrl: '../templates/study-locations.component.html',
  styles: []
})
export class StudyLocationsComponent implements OnInit {
  public studyLocations: Place[];
  public sub: any;
  public searchText: string = "";
  public sortOptionsVisible: boolean = false;

  constructor(private titleService: TitleService, private sortService: SortService, private placeService: PlaceService, private route: ActivatedRoute) { }

  ngOnInit() {
    this.titleService.setTitle('Study Locations');
     this.sub = this.route.queryParams.subscribe(params => {
        let sanitizedSearch = params['search']
        this.placeService.getStudyLocations(sanitizedSearch).subscribe(studyLocations =>{
            this.studyLocations = studyLocations['places']
        });
    });
  }


}
