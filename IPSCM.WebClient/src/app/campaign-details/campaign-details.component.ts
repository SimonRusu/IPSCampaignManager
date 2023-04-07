import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-campaign-details',
  templateUrl: './campaign-details.component.html',
  styleUrls: ['./campaign-details.component.sass']
})
export class CampaignDetailsComponent {
  campaign: any;
  campaignImage: any;
  

  constructor(private route: ActivatedRoute, private apiService: ApiService){
    this.route.queryParams.subscribe(params => {
      if(params['data']){
        this.campaign = JSON.parse(params['data']);
      }
    })
  }

  ngOnInit(){
    this.apiService.getCampaignImageById(this.campaign.Id).subscribe(
      campaignImage =>{
        const reader = new FileReader();
        reader.onload = () => {
          this.campaignImage = reader.result as string;
        };
        reader.readAsDataURL(campaignImage);
      }
    )
  }
}
