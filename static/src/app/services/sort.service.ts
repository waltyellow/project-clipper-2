import { Injectable }      from '@angular/core';

@Injectable()
export class SortService {
    
  public propertySort<T>(items:T[], property:string, reverse:boolean) : void {
    items.sort((a, b) => {
      if(a[property] < b[property]) return reverse? 1 : -1;
      else if (a[property] == b[property]) return 0;
      else return reverse? -1 : 1;
    })
  } 
}