import { Comment } from '../models/comment';
import { CommentService } from '../services/comment.service';
import { SortService } from '../services/sort.service';
import { Component, OnInit, Input } from '@angular/core';


@Component({
  selector: 'comment',
  templateUrl: '../templates/comment.component.html',
})

export class MessageComponent {
  public comments: Comment[]
  public questions: Comment[]
  public newComment : Comment
  public commentView: boolean = true;
  @Input() parentId: string;

  constructor(public commentService: CommentService) { }

  public postComment() : void {
    this.newComment.posted = new Date().getTime()
    this.newComment.parent = this.parentId
    this.newComment.type = this.commentView? 'comment' : 'question'
    this.commentService.postComment(this.newComment).subscribe(comment => (this.commentView? this.comments : this.questions).unshift(comment))
    this.newComment = this.emptyComment()
  }

  ngOnInit() {
    console.log(this.parentId);
    this.subscribeToComments()
    this.newComment = this.emptyComment()
  }
  
  private emptyComment() : Comment {
    return new Comment('', '', 0, 'demoUser', '', '', 0)
  }
  
  subscribeToComments() {
    this.commentService.getComments(this.parentId).subscribe(comments => {
        let messages = comments['messages']
        
        this.comments = messages.filter(msg => msg.type == 'comment')
        SortService.propertySort(this.comments, 'posted', true)
        
        this.questions = messages.filter(msg => msg.type == 'question')
        SortService.propertySort(this.questions, 'posted', true)
    })
  }
  
  setCommentView(commentView: boolean) {
    this.commentView = commentView;
  }
}
