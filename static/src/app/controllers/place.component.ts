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
  selector: 'app-place',
  templateUrl: '../templates/place.component.html',
})
export class PlaceComponent extends MessageComponent implements OnInit {
  public place: Place;
  private sub:any;

  constructor(private titleService: TitleService, private placeService: PlaceService, private commentSvc: CommentService,
        private route: ActivatedRoute, private sorter: SortService) {
    super(commentSvc, sorter)
  }

  public postComment() : void {
    super.postComment(this.place.place_id)
  }

  ngOnInit() {
    this.titleService.setTitle('Places');
    this.sub = this.route.params.subscribe(params => {
        let id = params['id'];
        this.placeService.getPlace(id).subscribe(place => this.place = place)
        this.subscribeToComments(id)
    });
    super.ngOnInit()
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }
}
