import { Component, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../services/api.service';
import JSZip from 'jszip';


@Component({
  selector: 'app-campaign-details',
  templateUrl: './campaign-details.component.html',
  styleUrls: ['./campaign-details.component.sass']
})
export class CampaignDetailsComponent {

  campaignImages: string[] = [];
  campaign: any;
  campaignImage: any;
  dongleName: any;
  sequence: any;
  captures: any;
  beaconConfs: any;
  beaconBleSignals: any;
  opt: number = 0;

  constructor(private route: ActivatedRoute, private apiService: ApiService){
    this.route.queryParams.subscribe(params => {
      if(params['data']){
        this.campaign = JSON.parse(params['data']);
      }
    })

    
 
  }

  ngOnInit(){
    this.getApiData();
  }


  getApiData(){
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

    this.apiService.getDongleName(this.campaign.Id_dongle).subscribe(
      dongleName =>{
        this.dongleName = dongleName;
      }
    )

    this.apiService.getCampaignSequence(this.campaign.Id_campaign_sequence).subscribe(
      sequence =>{
        this.sequence = sequence;
      }
    )

    this.apiService.getCaptures(this.campaign.Id).subscribe(
      captures =>{
        this.captures = captures;
      }
    )

    this.apiService.getSignals(this.campaign.Id).subscribe(
      signals =>{
        this.beaconBleSignals = signals;
      }
    )

    this.apiService.getConfigs(this.campaign.Id).subscribe(
      configs =>{
        this.beaconConfs = configs;
      }
    )


    
  }

  optionSelected(option: string){
    switch(option){
      case 'captures':
        this.opt = 1;
        break;
      case 'beacon_signal':
        this.opt = 2;
        break;
      case 'beacon_config':
        this.opt = 3;
        break;
    }
  }
}
