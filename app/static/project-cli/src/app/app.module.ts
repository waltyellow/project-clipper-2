import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { AlertModule } from 'ng2-bootstrap';

import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { routing } from './app.routing';
import { EventComponent } from './events/event.component';
import { EventsComponent } from './events/events.component';
import { EntertainmentsComponent } from './entertainments/entertainments.component';
import { BuildingsComponent } from './buildings/buildings.component';
import { StudyLocationsComponent } from './study-locations/study-locations.component';
import { QuestionsComponent } from './questions/questions.component'; 

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    EventComponent,
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
    routing
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
