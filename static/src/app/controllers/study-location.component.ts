import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { PlaceService } from '../services/place.service'
import {ActivatedRoute } from '@angular/router';
import { Place }        from '../models/place';
import { TitleService } from '../services/title.service';
import { CommentService } from '../services/comment.service';
import { MessageComponent } from './messages.component';

@Component({
  selector: 'app-study-location',
  templateUrl: '../templates/study-location.component.html',
})

export class StudyLocationComponent extends MessageComponent implements OnInit {
    public studyLocation: Place;
    private sub:any;

    constructor(private titleService: TitleService, private placeService: PlaceService, private commentSvc: CommentService,
        private route: ActivatedRoute) {
    super(commentSvc)
  }
    public postComment() : void {
        super.postComment(this.studyLocation.place_id)
  }

  ngOnInit() {
    this.titleService.setTitle('Study Spaces');
    this.sub = this.route.params.subscribe(params => {
        let id = params['id'];
        this.placeService.getPlace(id).subscribe(studyLocation => this.studyLocation = studyLocation)
        this.subscribeToComments(id)
    });
    super.ngOnInit()
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }

}
