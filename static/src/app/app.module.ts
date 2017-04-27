import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { AlertModule } from 'ng2-bootstrap';

import { AppComponent } from './app.component';
import { HomeComponent } from './controllers/home.component';
import { routing } from './app.routing';

import { EventComponent } from './controllers/event.component';
import { EventsComponent } from './controllers/events.component';
import { EntertainmentsComponent } from './controllers/entertainments.component';
import { PlaceComponent } from './controllers/place.component';
import { BuildingsComponent } from './controllers/buildings.component';
import { BuildingComponent } from './controllers/building.component';
import { StudyLocationsComponent } from './controllers/study-locations.component';
import { QuestionsComponent } from './controllers/questions.component';

import { EventService } from './services/event.service'
import { PlaceService } from './services/place.service';
import { TitleService } from './services/title.service';
import { CommentService } from './services/comment.service';
import { SortService } from './services/sort.service';


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    EventComponent,
    EventsComponent,
    EntertainmentsComponent,
    PlaceComponent,
    BuildingsComponent,
    BuildingComponent,
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
  providers: [EventService, TitleService, PlaceService, CommentService, SortService],
  bootstrap: [AppComponent]
})
export class AppModule { }
