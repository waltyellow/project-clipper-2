import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { PlaceService } from '../services/place.service'
import {ActivatedRoute } from '@angular/router';
import { Place }        from '../models/place';
import { TitleService } from '../services/title.service';
import { CommentService } from '../services/comment.service';
import { MessageComponent } from './messages.component';
import { SortService } from '../services/sort.service';

@Component({
  selector: 'app-building',
  templateUrl: '../templates/building.component.html',
})

export class BuildingComponent extends MessageComponent implements OnInit {
  public building: Place;
  private sub:any;

  constructor(private titleService: TitleService, private placeService: PlaceService, private commentSvc: CommentService,
        private route: ActivatedRoute, private sorter: SortService) {
    super(commentSvc, sorter)
  }
  
  public postComment() : void {
    console.log(this.building)
    console.log(this.building.place_id)
    super.postComment(this.building.place_id)
  }

  ngOnInit() {
    this.titleService.setTitle('Buildings');
    this.sub = this.route.params.subscribe(params => {
        let id = params['id'];
        console.log(id)
        this.placeService.getPlace(id).subscribe(building => this.building = building)
        this.subscribeToComments(id)
    });
    super.ngOnInit()
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }
}
