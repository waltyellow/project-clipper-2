import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { AlertModule } from 'ng2-bootstrap';

import { AppComponent } from './app.component';
import { MenuComponent } from './menu.component';
import { CONST_ROUTING } from './app.routing';
import { EventsComponent } from './events/events.component';
import { EntertainmentsComponent } from './entertainments/entertainments.component';
import { BuildingsComponent } from './buildings/buildings.component';
import { StudyLocationsComponent } from './study-locations/study-locations.component';
import { QuestionsComponent } from './questions/questions.component'; 

@NgModule({
  declarations: [
    AppComponent,
    MenuComponent,
    EventsComponent,
    EntertainmentsComponent,
    BuildingsComponent,
    StudyLocationsComponent,
    QuestionsComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AlertModule.forRoot(),
    CONST_ROUTING
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
