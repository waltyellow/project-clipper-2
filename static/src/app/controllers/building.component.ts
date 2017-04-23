import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { BuildingService } from '../services/building.service'
import {ActivatedRoute } from '@angular/router';
import { Building }        from '../models/building';
import { Comment }         from '../models/comment';
import { TitleService } from '../services/title.service';
import { CommentService } from '../services/comment.service';

@Component({
  selector: 'app-building',
  templateUrl: '../templates/building.component.html',
})

export class BuildingComponent implements OnInit {
  public building: Building;
  public comments: Comment[]
  public newComment : Comment
  private sub:any;

  constructor(private titleService: TitleService, private buildingService: BuildingService, private commentService: CommentService, private route: ActivatedRoute) { }

  public postComment() : void {
    this.commentService.postComment(this.newComment).subscribe(comment => this.comments.push(comment))
    this.newComment = new Comment('', '', '', 'demoUser')
  }

  ngOnInit() {
    this.titleService.setTitle('Buildings');
    this.sub = this.route.params.subscribe(params => {
        let id = params['id'];
        this.buildingService.getEvent(id).subscribe(building => this.building = building)
        this.commentService.getComments(id).subscribe(comments => this.comments = comments['messages'])
    });
    this.newComment = new Comment('', '', '', 'demoUser')
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }
}
