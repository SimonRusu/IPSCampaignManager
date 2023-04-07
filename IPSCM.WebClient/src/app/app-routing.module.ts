import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { UploadCampaignComponent } from './upload-campaign/upload-campaign.component';
import { CampaignDetailsComponent } from './campaign-details/campaign-details.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent},
  { path: 'upload-campaign', component: UploadCampaignComponent },
  { path: 'campaign-details', component: CampaignDetailsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
