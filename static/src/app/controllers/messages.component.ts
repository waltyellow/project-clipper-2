import { Comment } from '../models/comment';
import { CommentService } from '../services/comment.service';
import { SortService } from '../services/sort.service';

export class MessageComponent {
  public comments: Comment[]
  public questions: Comment[]
  public newComment : Comment
  public commentView: boolean = true;

  constructor(public commentService: CommentService) { }

  public postComment(parentId: string) : void {
    this.newComment.posted = new Date().getTime()
    this.newComment.parent = parentId
    this.newComment.type = this.commentView? 'comment' : 'question'
    this.commentService.postComment(this.newComment).subscribe(comment => (this.commentView? this.comments : this.questions).unshift(comment))
    this.newComment = this.emptyComment()
  }

  ngOnInit() {
    this.newComment = this.emptyComment()
  }
  
  private emptyComment() : Comment {
    return new Comment('', '', 0, 'demoUser', '', '', 0)
  }
  
  subscribeToComments(id) {
    this.commentService.getComments(id).subscribe(comments => {
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
