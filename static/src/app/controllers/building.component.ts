import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { BuildingService } from '../services/building.service'
import {ActivatedRoute } from '@angular/router';
import { Building }        from '../models/building';
import { TitleService } from '../services/title.service';
import { CommentService } from '../services/comment.service';
import { MessageComponent } from './messages.component';
import { SortService } from '../services/sort.service';

@Component({
  selector: 'app-building',
  templateUrl: '../templates/building.component.html',
})

export class BuildingComponent extends MessageComponent implements OnInit {
  public building: Building;
  private sub:any;

  constructor(private titleService: TitleService, private buildingService: BuildingService, private commentSvc: CommentService,
        private route: ActivatedRoute, private sorter: SortService) {
    super(commentSvc, sorter)
  }
  
  public postComment() : void {
    super.postComment(this.building.buildingId)
  }

  ngOnInit() {
    this.titleService.setTitle('Buildings');
    this.sub = this.route.params.subscribe(params => {
        let id = params['id'];
        this.buildingService.getBuilding(id).subscribe(building => this.building = building)
        this.subscribeToComments(id)
    });
    super.ngOnInit()
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }
}
