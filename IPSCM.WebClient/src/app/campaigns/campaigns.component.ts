import { Component } from '@angular/core';
import { ApiService } from '../services/api.service';
import { toArray } from 'rxjs';

@Component({
  selector: 'app-campaigns',
  templateUrl: './campaigns.component.html',
  styleUrls: ['./campaigns.component.sass']
})
export class CampaignsComponent {
  campaigns: any = [];
  p: number = 1;

  constructor(private apiService: ApiService){

  }

  ngOnInit(){
    this.apiService.getCampaigns().subscribe(data => {
      this.campaigns = data;
    });

  }
}
