import { Component, OnInit } from '@angular/core';
import { TitleService } from '../services/title.service';

@Component({
  selector: 'app-study-locations',
  templateUrl: '../templates/study-locations.component.html',
  styles: []
})
export class StudyLocationsComponent implements OnInit {

  constructor(private titleService: TitleService) { }

  ngOnInit() {
    this.titleService.setTitle('Study Locations');
  }

}
