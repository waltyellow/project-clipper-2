import { Injectable }      from '@angular/core';

@Injectable()
export class SortService {
    
  public propertySort<T>(items:T[], property:string) : void {
    items.sort((a, b) => {
      (console.log(a[property]))
      if(a[property] < b[property]) return -1;
      else if (a[property] == b[property]) return 0;
      else return 1;
    })
  } 
}