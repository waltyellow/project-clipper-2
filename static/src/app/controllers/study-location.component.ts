import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { PlaceService } from '../services/place.service'
import {ActivatedRoute } from '@angular/router';
import { Place }        from '../models/place';
import { TitleService } from '../services/title.service';

@Component({
  selector: 'app-study-location',
  templateUrl: '../templates/study-location.component.html',
})

export class StudyLocationComponent implements OnInit {
    public studyLocation: Place;
    private sub:any;
    private parentId : string;

    constructor(private titleService: TitleService, private placeService: PlaceService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.titleService.setTitle('Study Spaces');
    this.sub = this.route.params.subscribe(params => {
        this.parentId = params['id'];
        this.placeService.getPlace(this.parentId).subscribe(studyLocation => this.studyLocation = studyLocation)
    });
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }

}
