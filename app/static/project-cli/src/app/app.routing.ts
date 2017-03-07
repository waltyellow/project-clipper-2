import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from "./home/home.component";
import { EntertainmentsComponent } from "./entertainments/entertainments.component";
import { EventsComponent } from "./events/events.component";
import { EventComponent } from "./events/event.component";
import { BuildingsComponent } from "./buildings/buildings.component";
import { QuestionsComponent } from "./questions/questions.component";
import { StudyLocationsComponent } from "./study-locations/study-locations.component";

const MAINMENU_ROUTES: Routes = [
    //full : makes sure the path is absolute path
    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: 'home', component: HomeComponent },
    { path: 'food-and-entertainments', component: EntertainmentsComponent },
    { path: 'events', component: EventsComponent },
    { path: 'events/:id/event', component: EventComponent },
    { path: 'buildings', component: BuildingsComponent },
    { path: 'questions', component: QuestionsComponent },
    { path: 'study-locations', component: StudyLocationsComponent }
];
export const routing = RouterModule.forRoot(MAINMENU_ROUTES);