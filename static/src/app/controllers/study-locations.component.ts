import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { TitleService } from '../services/title.service';
import { PlaceService } from '../services/place.service';
import { Place }        from '../models/place';
import { SortService } from '../services/sort.service';

@Component({
  selector: 'app-study-locations',
  templateUrl: '../templates/study-locations.component.html',
  styles: []
})
export class StudyLocationsComponent implements OnInit {
  public listView: boolean = true;
  public studyLocations: Place[];

  constructor(private titleService: TitleService, private sortService: SortService, private placeService: PlaceService) { }

  ngOnInit() {
    this.titleService.setTitle('Study Locations');
    this.placeService.getStudyLocations().subscribe(studyLocations => this.studyLocations = studyLocations['places']);
  }
  setListView(listView: boolean){
    this.listView = listView;
  }

}
