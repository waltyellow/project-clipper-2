import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from "./controllers/home.component";
import { EntertainmentsComponent } from "./controllers/entertainments.component";
import { PlaceComponent } from "./controllers/place.component";
import { EventsComponent } from "./controllers/events.component";
import { EventComponent } from "./controllers/event.component";
import { BuildingsComponent } from "./controllers/buildings.component";
import { BuildingComponent } from "./controllers/building.component";
import { QuestionsComponent } from "./controllers/questions.component";
import { StudyLocationsComponent } from "./controllers/study-locations.component";

const MAINMENU_ROUTES: Routes = [
    //full : makes sure the path is absolute path
    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: 'home', component: HomeComponent },
    { path: 'places', component: EntertainmentsComponent },
    { path: 'places/:id/place', component: PlaceComponent },
    { path: 'events', component: EventsComponent },
    { path: 'events/:id/event', component: EventComponent },
    { path: 'campus-buildings/:id/campus-buildings', component: BuildingComponent },
    { path: 'campus-buildings', component: BuildingsComponent },
    { path: 'questions', component: QuestionsComponent },
    { path: 'study-locations', component: StudyLocationsComponent }
];
export const routing = RouterModule.forRoot(MAINMENU_ROUTES);
