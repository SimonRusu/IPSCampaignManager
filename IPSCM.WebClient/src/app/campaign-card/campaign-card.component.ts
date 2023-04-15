import { Component, Input } from '@angular/core';
import { ApiService } from '../services/api.service';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmationDialogComponent } from '../confirmation-dialog/confirmation-dialog.component';
import { ToastrService } from 'ngx-toastr';
import { catchError, of, tap } from 'rxjs';
import { Router } from '@angular/router';
import JSZip from 'jszip';



@Component({
  selector: 'app-campaign-card',
  templateUrl: './campaign-card.component.html',
  styleUrls: ['./campaign-card.component.sass']
})
export class CampaignCardComponent {
  @Input() campaign!: any;
  campaignImages: string[] = [];
  

  constructor(
    private apiService: ApiService, 
    private dialog: MatDialog,
    private toastr: ToastrService, 
    private router: Router){

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
  
  stringifyCampaign() {
    return JSON.stringify(this.campaign);
  }


  deleteConfirmDialog(){
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: '400px',
      data: 'Esta acción borrará la campaña seleccionada y no se puede deshacer.'
    })

    dialogRef.afterClosed().subscribe(res =>{
      if(res){
        this.apiService.deleteCampaignById(this.campaign.Id).pipe(
          tap(() => {
              this.toastr.success('¡La campaña se ha borrado correctamente!', 'Operación completada');
              this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
                this.router.navigate(['/campaigns'])
              });
            }),
            catchError(() => {
              this.toastr.error('Ha ocurrido un error durante el borrado', 'Operación no completada');
              return of(null);
            })
          ).subscribe();
      }
    })
  }
}