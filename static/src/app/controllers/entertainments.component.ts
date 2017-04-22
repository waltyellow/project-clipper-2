import { Component, OnInit } from '@angular/core';   
import {ViewEncapsulation} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { PlaceService } from '../services/place.service';
import { TitleService } from '../services/title.service';
import { Place }        from '../models/place';

@Component({
  selector: 'app-events',
  templateUrl: '../templates/entertainments.component.html',
})
export class EntertainmentsComponent implements OnInit {
  public places: Place[];
  
  constructor(private titleService: TitleService, private placeService: PlaceService) {
  }

  ngOnInit() {
    this.titleService.setTitle('Events');
    this.placeService.getPlaces().subscribe(places => this.places = places['places']);
  }
}
