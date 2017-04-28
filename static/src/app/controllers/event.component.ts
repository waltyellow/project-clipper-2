import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { EventService } from '../services/event.service'
import {ActivatedRoute } from '@angular/router';
import { Eventx }        from '../models/eventx';
import { TitleService } from '../services/title.service';
import { CommentService } from '../services/comment.service';
import { MessageComponent } from './messages.component';

@Component({
  selector: 'app-event',
  templateUrl: '../templates/event.component.html',
})
export class EventComponent extends MessageComponent implements OnInit {
  public event: Eventx;
  private sub:any;

  constructor(private titleService: TitleService, private eventService: EventService, private commentSvc: CommentService,
          private route: ActivatedRoute) {
    super(commentSvc)
  }
  
  public postComment() {
    super.postComment(this.event.event_id)
  }

  ngOnInit() {
    this.titleService.setTitle('Events');
    this.sub = this.route.params.subscribe(params => {
        let id = params['id'];
        this.eventService.getEvent(id).subscribe(event => this.event = event)
        this.subscribeToComments(id)
    });
    super.ngOnInit()
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }
}
