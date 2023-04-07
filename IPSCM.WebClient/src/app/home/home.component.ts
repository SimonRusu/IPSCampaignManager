import { Component } from '@angular/core';
import { ApiService } from '../services/api.service';
import { toArray } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.sass']
})
export class HomeComponent {
  campaigns: any = [];

  constructor(private apiService: ApiService){

  }

  ngOnInit(){
    this.apiService.getCampaigns().subscribe(data => {
      this.campaigns = data;
    });

  }
}
