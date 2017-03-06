import { Routes, RouterModule } from '@angular/router';
import { EntertainmentsComponent } from "./entertainments/entertainments.component";
import { EventsComponent } from "./events/events.component";
import { BuildingsComponent } from "./buildings/buildings.component";
import { QuestionsComponent } from "./questions/questions.component";
import { StudyLocationsComponent } from "./study-locations/study-locations.component";
const MAINMENU_ROUTES: Routes = [
    //full : makes sure the path is absolute path
    { path: 'food-and-entertainments', component: EntertainmentsComponent },
    { path: 'events', component: EventsComponent },
    { path: 'buildings', component: BuildingsComponent },
    { path: 'questions', component: QuestionsComponent },
    { path: 'study-locations', component: StudyLocationsComponent }
];
export const CONST_ROUTING = RouterModule.forRoot(MAINMENU_ROUTES);