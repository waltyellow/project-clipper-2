import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { TitleService } from '../services/title.service';
import { PlaceService } from '../services/place.service';
import { Place }        from '../models/place';
import { SortService } from '../services/sort.service';

@Component({
  selector: 'app-buildings',
  templateUrl: '../templates/buildings.component.html',
  styles: []
})
export class BuildingsComponent implements OnInit {
  public listView: boolean = true;
  public buildings: Place[];

  constructor(private titleService: TitleService, private sortService: SortService, private placeService: PlaceService) {
  }
  ngOnInit() {
    this.titleService.setTitle('Campus Buildings');
    this.placeService.getBuildings().subscribe(buildings => this.buildings = buildings['places']);
  }

  public sortBuildings(){
    this.sortService.propertySort<Place>(this.buildings, 'name');
  }

  setListView(listView: boolean){
    this.listView = listView;
  }
}
