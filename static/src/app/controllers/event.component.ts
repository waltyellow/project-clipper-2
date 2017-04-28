import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { EventService } from '../services/event.service'
import {ActivatedRoute } from '@angular/router';
import { Eventx }        from '../models/eventx';
import { TitleService } from '../services/title.service';
import { CommentService } from '../services/comment.service';

@Component({
  selector: 'app-event',
  templateUrl: '../templates/event.component.html',
})
export class EventComponent implements OnInit {
  public event: Eventx;
  private sub:any;
  private parentId : string;

  constructor(private titleService: TitleService, private eventService: EventService, private commentSvc: CommentService,
          private route: ActivatedRoute) {
  }
 
  ngOnInit() {
    this.titleService.setTitle('Events');
    this.sub = this.route.params.subscribe(params => {
        this.parentId = params['id'];
        this.eventService.getEvent(this.parentId).subscribe(event => this.event = event)
        //this.subscribeToComments(this.parentId)
    });
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }
}
