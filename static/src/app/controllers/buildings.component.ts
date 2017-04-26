import { Component, OnInit } from '@angular/core';
import {ViewEncapsulation} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { TitleService } from '../services/title.service';
import { BuildingService } from '../services/building.service';
import { Building }        from '../models/building';
import { SortService } from '../services/sort.service';

@Component({
  selector: 'app-buildings',
  templateUrl: '../templates/buildings.component.html',
  styles: []
})
export class BuildingsComponent implements OnInit {
  public listView: boolean = true;
  public buildings: Building[];

  constructor(private titleService: TitleService, private sortService: SortService, private buildingService: BuildingService) {
  }
  ngOnInit() {
    this.titleService.setTitle('Campus Buildings');
    this.buildingService.getBuildings().subscribe(buildings => this.buildings = buildings['buildings']);
  }

  public sortBuildings(){
    this.sortService.propertySort<Building>(this.buildings, 'name');
  }

  setListView(listView: boolean){
    this.listView = listView;
  }
}
