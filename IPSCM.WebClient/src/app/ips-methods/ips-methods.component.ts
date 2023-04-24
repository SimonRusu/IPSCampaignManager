import { Component } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-ips-methods',
  templateUrl: './ips-methods.component.html',
  styleUrls: ['./ips-methods.component.sass']
})
export class IpsMethodsComponent {
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
