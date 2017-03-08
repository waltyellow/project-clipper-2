import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { EventService } from './event.service'
import {ActivatedRoute } from '@angular/router';
import { Eventx }        from './eventx';

@Component({
  selector: 'app-event',
  templateUrl: './event.component.html',
})
export class EventComponent implements OnInit {
  public event: Eventx;
  private sub:any;

  constructor(private eventService: EventService, private route: ActivatedRoute) { }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
        let id = params['id'];
        this.eventService.getEvent(id).subscribe(event => this.event = event)
    });
  }

  ngOnDestroy() {
    // Clean sub to avoid memory leak
    this.sub.unsubscribe();
  }
}
