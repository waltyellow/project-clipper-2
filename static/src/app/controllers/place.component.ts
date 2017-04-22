import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { PlaceService } from '../services/place.service'
import {ActivatedRoute } from '@angular/router';
import { Place }        from '../models/place';
import { Comment }         from '../models/comment';
import { TitleService } from '../services/title.service';
import { CommentService } from '../services/comment.service';

@Component({
  selector: 'app-place',
  templateUrl: '../templates/place.component.html',
})
export class PlaceComponent implements OnInit {
  public place: Place;
  public comments: Comment[]
  public newComment : Comment
  private sub:any;

  constructor(private titleService: TitleService, private placeService: PlaceService, private commentService: CommentService, private route: ActivatedRoute) { }

  public postComment() : void {
    this.commentService.postComment(this.newComment).subscribe(comment => this.comments.push(comment))
    this.newComment = new Comment('', '', '', 'demoUser')
  }

  ngOnInit() {
    this.titleService.setTitle('Places');
    this.sub = this.route.params.subscribe(params => {
        let id = params['id'];
        this.placeService.getPlace(id).subscribe(place => this.place = place)
        this.commentService.getComments(id).subscribe(comments => this.comments = comments['messages'])
    });
    this.newComment = new Comment('', '', '', 'demoUser')
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }
}
