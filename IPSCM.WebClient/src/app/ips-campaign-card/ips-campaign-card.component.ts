import { Component, Input } from '@angular/core';
import { ApiService } from '../services/api.service';
import JSZip from 'jszip';


@Component({
  selector: 'app-ips-campaign-card',
  templateUrl: './ips-campaign-card.component.html',
  styleUrls: ['./ips-campaign-card.component.sass']
})


export class IpsCampaignCardComponent {
  @Input() campaign!: any;
  campaignImages: string[] = [];
  operaciones: string[] = ['op1', 'op2', 'op3'];
  seleccionada: string = this.operaciones[0];



  constructor(
    private apiService: ApiService){}


    formatLabel(value: number): string {
      if (value >= 1000) {
        return Math.round(value / 1000) + 'k';
      }
  
      return `${value}`;
    }
  
    ngOnInit(){
      this.apiService.getCampaignImagesById(this.campaign.Id).subscribe((response: Blob) => {
        const zipImages = new JSZip();
        zipImages.loadAsync(response).then(images =>{
          Object.keys(images.files).forEach(filename => {
            images.files[filename].async('base64').then(imageData => {
              const imageUrl = 'data:image/jpeg;base64,' + imageData;
              this.campaignImages.push(imageUrl);
            })
          })
        })
      })
    }


}
