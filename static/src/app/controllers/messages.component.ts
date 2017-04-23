import { Comment } from '../models/comment';
import { CommentService } from '../services/comment.service';

export class MessageComponent {
  public comments: Comment[]
  public questions: Comment[]
  public newComment : Comment
  public commentView: boolean = true;

  constructor(public commentService: CommentService) { }

  public postComment(parentId: string) : void {
    this.newComment.message_timestamp = new Date().getTime()
    this.newComment.message_parent = parentId
    this.newComment.message_type = this.commentView? 'comment' : 'question'
    this.commentService.postComment(this.newComment).subscribe(comment => this.comments.push(comment))
    this.newComment = this.emptyComment()
  }

  ngOnInit() {
    this.newComment = this.emptyComment()
  }
  
  private emptyComment() : Comment {
    return new Comment('', '', 0, 'demoUser', '', '')
  }
  
  subscribeToComments(id) {
    this.commentService.getComments(id).subscribe(comments => {
        let messages = comments['messages']
        this.comments = messages.filter(msg => msg.message_type == 'comment')
        this.questions = messages.filter(msg => msg.message_type == 'question')
    })
  }
  
  setCommentView(commentView: boolean) {
    this.commentView = commentView;
  }
}
