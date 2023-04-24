import { Component, Input } from '@angular/core';
import { ApiService } from '../services/api.service';
import JSZip from 'jszip';
import { ThemePalette } from '@angular/material/core';

export interface Task {
  name: string;
  completed: boolean;
  color: ThemePalette;
  subtasks?: Task[];
}

@Component({
  selector: 'app-ips-campaign-card',
  templateUrl: './ips-campaign-card.component.html',
  styleUrls: ['./ips-campaign-card.component.sass']
})


export class IpsCampaignCardComponent {
  @Input() campaign!: any;
  campaignImages: string[] = [];
  allComplete: boolean = false;

  task: Task = {
    name: 'Aplicar todos los métodos IPS',
    completed: false,
    color: 'warn',
    subtasks: [
      {name: 'Fingerprinting (WKNN)', completed: false, color: 'primary'},
      {name: 'Redes neuronales', completed: false, color: 'primary'},
      {name: 'Método adicional', completed: false, color: 'primary'},
    ],
  };

  constructor(
    private apiService: ApiService){}
  
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

  updateAllComplete() {
    this.allComplete = this.task.subtasks != null && this.task.subtasks.every(t => t.completed);
  }

  someComplete(): boolean {
    if (this.task.subtasks == null) {
      return false;
    }
    return this.task.subtasks.filter(t => t.completed).length > 0 && !this.allComplete;
  }

  setAll(completed: boolean) {
    this.allComplete = completed;
    if (this.task.subtasks == null) {
      return;
    }
    this.task.subtasks.forEach(t => (t.completed = completed));
  }


}
