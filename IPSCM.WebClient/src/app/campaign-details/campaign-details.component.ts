import { Component, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../services/api.service';
import JSZip from 'jszip';
import { OwlOptions } from 'ngx-owl-carousel-o';
import { Observable, forkJoin, map, switchMap } from 'rxjs';


@Component({
  selector: 'app-campaign-details',
  templateUrl: './campaign-details.component.html',
  styleUrls: ['./campaign-details.component.sass',
              ],
  providers: [],
})
export class CampaignDetailsComponent {

  campaignImages: string[] = [];
  campaign: any;
  campaignDetails: any;
  relatedCampaign: any;
  dongleName: any;
  sequence: any;
  captures: any;
  beaconConfs: any;
  beaconBleSignals: any;
  opt: number = 0;
  switchData: boolean = false;
  loading: boolean = true;

  customOptions: OwlOptions = {
    loop: true,
    smartSpeed: 1000,
    autoplayTimeout: 6000,
    autoplay: true,
    mouseDrag: true,
    touchDrag: false,
    pullDrag: false,
    dots: true,
    navText: ['', ''],
    responsive: {
      0: {
        items: 1
      },
      400: {
        items: 2
      },
      740: {
        items: 3
      }
    },
    nav: false
  }

  constructor(private route: ActivatedRoute, private apiService: ApiService){
    this.route.queryParams.subscribe(params => {
      if(params['data']){
        this.campaign = JSON.parse(params['data']);
      }
    })

    apiService.getCampaignImagesById(this.campaign.Id).subscribe((response: Blob) => {
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

    this.campaignData().subscribe(res =>{
      this.campaignDetails = res
      this.loading=false;})
      
    this.relatedCampaignData().subscribe(res => {this.relatedCampaign = res});
  }

  campaignData(): Observable<any> {
    return forkJoin([
        this.apiService.getDongleName(this.campaign.Id_dongle),
        this.apiService.getCampaignSequence(this.campaign.Id_campaign_sequence),
        this.apiService.getCaptures(this.campaign.Id),
        this.apiService.getSignals(this.campaign.Id)
    ]).pipe(
        map(([dongleName, campaignSequence, captures, signals]) => {
            return {
                dongleName,
                campaignSequence,
                captures,
                signals
            };
            
        })
        
      );
  }
  
  relatedCampaignData(): Observable<any> {
    return this.apiService.getRelatedCampaignById(this.campaign.Id_related_campaign).pipe(
      switchMap((relatedCampaign: any) => {
        return forkJoin([
          this.apiService.getDongleName(relatedCampaign.Id_dongle),
          this.apiService.getCampaignSequence(relatedCampaign.Id_campaign_sequence),
          this.apiService.getCaptures(relatedCampaign.Id),
          this.apiService.getSignals(relatedCampaign.Id)
        ]).pipe(
          map(([dongleName, campaignSequence, captures, signals]) => {
            relatedCampaign.dongleName = dongleName;
            relatedCampaign.campaignSequence = campaignSequence;
            relatedCampaign.captures = captures;
            relatedCampaign.signals = signals;
            return relatedCampaign;
          })
        );
      })
    );
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
