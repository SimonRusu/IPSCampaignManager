import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CampaignsComponent } from './campaigns/campaigns.component';
import { UploadCampaignComponent } from './upload-campaign/upload-campaign.component';
import { CampaignDetailsComponent } from './campaign-details/campaign-details.component';
import { IpsMethodsComponent } from './ips-methods/ips-methods.component';
const routes: Routes = [
  { path: 'campaigns', component: CampaignsComponent},
  { path: 'upload-campaign', component: UploadCampaignComponent },
  { path: 'campaign-details', component: CampaignDetailsComponent },
  { path: 'ips-methods', component: IpsMethodsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
