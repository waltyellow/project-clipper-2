import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { EventService } from '../services/event.service'
import {ActivatedRoute } from '@angular/router';
import { Eventx }        from '../models/eventx';
import { Comment }         from '../models/comment';
import { TitleService } from '../services/title.service';
import { CommentService } from '../services/comment.service'; 

@Component({
  selector: 'app-event',
  templateUrl: '../templates/event.component.html',
})
export class EventComponent implements OnInit {
  public event: Eventx;
  public comments: Comment[]
  public newComment : Comment
  private sub:any;

  constructor(private titleService: TitleService, private eventService: EventService, private commentService: CommentService, private route: ActivatedRoute) { }

  public postComment() : void {
    this.commentService.postComment(this.newComment).subscribe(comment => this.comments.push(comment))
    this.newComment = new Comment('', '', '', 'demoUser')
  }

  ngOnInit() {
    this.titleService.setTitle('Events');
    this.sub = this.route.params.subscribe(params => {
        let id = params['id'];
        this.eventService.getEvent(id).subscribe(event => this.event = event)
        this.commentService.getComments(id).subscribe(comments => this.comments = comments['messages'])
    });
    this.newComment = new Comment('', '', '', 'demoUser')
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }
}
