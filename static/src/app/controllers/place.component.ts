import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { PlaceService } from '../services/place.service'
import {ActivatedRoute } from '@angular/router';
import { Place }        from '../models/place';
import { TitleService } from '../services/title.service';

@Component({
  selector: 'app-place',
  templateUrl: '../templates/place.component.html',
})
export class PlaceComponent implements OnInit {
  public place: Place;
  private sub:any;
  private parentId : string;

  constructor(private titleService: TitleService, private placeService: PlaceService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.titleService.setTitle('Food & Entertainment');
    this.sub = this.route.params.subscribe(params => {
        this.parentId = params['id'];
        this.placeService.getPlace(this.parentId).subscribe(place => this.place = place)
    });
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }
}
