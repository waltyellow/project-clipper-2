import { Component, OnInit } from '@angular/core';
import { TitleService } from '../services/title.service';

@Component({
  selector: 'app-entertainments',
  templateUrl: '../templates/entertainments.component.html',
})
export class EntertainmentsComponent implements OnInit {

  constructor(private titleService: TitleService) { }

  ngOnInit() {
    this.titleService.setTitle('Places');
  }

}
