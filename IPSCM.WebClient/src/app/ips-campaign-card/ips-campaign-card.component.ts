import { Component, Input } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-ips-campaign-card',
  templateUrl: './ips-campaign-card.component.html',
  styleUrls: ['./ips-campaign-card.component.sass']
})

export class IpsCampaignCardComponent {
  @Input() campaign!: any;
  campaignImage: any;


constructor(
  private apiService: ApiService){}

  ngOnInit(){
    this.apiService.getCampaignImagesById(this.campaign.Id).subscribe(
      apiService =>{
        const reader = new FileReader();
        reader.onload = () => {
          this.campaignImage = reader.result as string;
        };
        reader.readAsDataURL(apiService);
      }
    )
  }
}
