import { Component, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../services/api.service';
import JSZip from 'jszip';
import { OwlOptions } from 'ngx-owl-carousel-o';
import { Observable, forkJoin, map, switchMap } from 'rxjs';
import { MatButtonToggleChange } from '@angular/material/button-toggle';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';



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
  relatedCampaignDetails: any;
  selectedCamaign: any;
  dongleName: any;
  sequence: any;
  captures: any;
  beaconConfs: any;
  beaconBleSignals: any;
  opt: number = 1;
  loadingCampaign: boolean = true;
  loading: boolean = true;
  defaultPageSize = 10;
  pageSizes = [10, 25, 50, 100];
  capturesDataSource = new MatTableDataSource<any>([]);
  signalsDataSource = new MatTableDataSource<any>([]);
  capturesPageIndex: number = 0;
  signalsPageIndex: number = 0;
  capturesColumns = ['Id', 'Date', 'Light', 'Temperature', 'Relative_humidity', 'Absolute_humidity', 'Position_x', 'Position_y', 'Position_z', 'Platform_angle', 'Dongle_rotation'];
  signalsColumns = ['Id', 'N_reading', 'Date_hour', 'Mac', 'Pack_size', 'Channel', 'RSSI', 'PDU_type', 'CRC', 'Protocol', 'Identificator']
  @ViewChild('capturesPaginator') capturesPaginator?: MatPaginator;
  @ViewChild('signalsPaginator') signalsPaginator?: MatPaginator;
  @ViewChild('capturesTable') capturesTable: MatTable<any> | undefined;
  @ViewChild('signalsTable') signalsTable: MatTable<any> | undefined;

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
    nav: false,
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
        let count = 0;
        Object.keys(images.files).forEach(filename => {
          images.files[filename].async('base64').then(imageData => {
            const imageUrl = 'data:image/jpeg;base64,' + imageData;
            if (count < 3 && Object.keys(images.files).length == 1) {
              for (let i = 0; i < 2; i++) {
                this.campaignImages.push(imageUrl);
                count++;
              }
            } else {
              this.campaignImages.push(imageUrl);
              count++;
            }
          })
        })
      })
    })
    
  
    this.campaignData().subscribe(res =>{
      this.campaignDetails = this.selectedCamaign = res
      this.capturesDataSource.data = this.campaignDetails.captures;
      this.signalsDataSource.data = this.campaignDetails.signals;
    })
      
    this.relatedCampaignData().subscribe(res => {
      this.relatedCampaignDetails = res
      this.loading=false;
    });
  }

  ngAfterViewInit() {
    if (this.capturesPaginator) {
      this.capturesDataSource.paginator = this.capturesPaginator;
    }
    if (this.signalsPaginator) {
      this.signalsDataSource.paginator = this.signalsPaginator;
    }
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

  switchCampaignData(event: MatButtonToggleChange){
    if(event.value === 'aleatory'){
      this.selectedCamaign = this.campaignDetails;
      this.capturesDataSource.data = this.campaignDetails.captures;
      this.signalsDataSource.data = this.campaignDetails.signals;
    }else{
      this.selectedCamaign = this.relatedCampaignDetails;
      this.capturesDataSource.data = this.relatedCampaignDetails.captures;
      this.signalsDataSource.data = this.relatedCampaignDetails.signals;
    }

    if (this.capturesTable) {
      this.capturesTable.renderRows();
    }
    if (this.signalsTable) {
      this.signalsTable.renderRows();
    }
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
