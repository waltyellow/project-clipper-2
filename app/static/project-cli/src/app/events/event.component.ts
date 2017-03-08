import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { EventService } from './event.service'
import {ActivatedRoute } from '@angular/router';
import { Eventx }        from './eventx';
import { Comment }         from './comment';

@Component({
  selector: 'app-event',
  templateUrl: './event.component.html',
})
export class EventComponent implements OnInit {
  public event: Eventx;
  public comments: Comment[]
  public newComment : Comment
  private sub:any;

  constructor(private eventService: EventService, private route: ActivatedRoute) { }

  public postComment() : void {
    this.eventService.postComment(this.newComment).subscribe(comment => this.comments.push(comment))
    this.newComment = new Comment('', '', '', 'demoUser')
  }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
        let id = params['id'];
        this.eventService.getEvent(id).subscribe(event => this.event = event)
        this.eventService.getComments(id).subscribe(comments => this.comments = comments['messages'])
    });
    this.newComment = new Comment('', '', '', 'demoUser')
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }
}
