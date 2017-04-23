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
  public questions: Comment[]
  public newComment : Comment
  public commentView: boolean = true;
  private sub:any;

  constructor(private titleService: TitleService, private eventService: EventService, private commentService: CommentService, private route: ActivatedRoute) { }

  public postComment() : void {
    this.newComment.message_timestamp = new Date().getTime()
    this.newComment.message_parent = this.event.eventId
    this.newComment.message_type = this.commentView? 'comment' : 'question'
    this.commentService.postComment(this.newComment).subscribe(comment => this.comments.push(comment))
    this.newComment = this.emptyComment()
  }

  ngOnInit() {
    this.titleService.setTitle('Events');
    this.sub = this.route.params.subscribe(params => {
        let id = params['id'];
        this.eventService.getEvent(id).subscribe(event => this.event = event)
        this.commentService.getComments(id).subscribe(comments => {
            let messages = comments['messages']
            this.comments = messages.filter(msg => msg.message_type == 'comment')
            this.questions = messages.filter(msg => msg.message_type == 'question')
        })
    });
    this.newComment = this.emptyComment()
  }
  
  private emptyComment() : Comment {
    return new Comment('', '', 0, 'demoUser', '', '')
  }
  
    setCommentView(commentView: boolean) {
  	 this.commentView = commentView;
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }
}
