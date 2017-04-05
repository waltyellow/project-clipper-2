import { Component, OnInit } from '@angular/core';
import { TitleService } from '../services/title.service';

@Component({
  selector: 'app-buildings',
  templateUrl: '../templates/buildings.component.html',
  styles: []
})
export class BuildingsComponent implements OnInit {

  constructor(private titleService: TitleService) { }

  ngOnInit() {
    this.titleService.setTitle('Campus Buildings');
  }

}
