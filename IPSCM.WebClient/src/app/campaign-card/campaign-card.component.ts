import { Component, Input } from '@angular/core';
import { ApiService } from '../services/api.service';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmationDialogComponent } from '../confirmation-dialog/confirmation-dialog.component';
import { ToastrService } from 'ngx-toastr';
import { catchError, of, tap } from 'rxjs';
import { Router } from '@angular/router';



@Component({
  selector: 'app-campaign-card',
  templateUrl: './campaign-card.component.html',
  styleUrls: ['./campaign-card.component.sass']
})
export class CampaignCardComponent {
  @Input() campaign!: any;
  campaignImage: any;
  

  constructor(
    private apiService: ApiService, 
    private dialog: MatDialog,
    private toastr: ToastrService, 
    private router: Router){

  }

  ngOnInit(){
    this.apiService.getCampaignImageById(this.campaign.Id).subscribe(
      apiService =>{
        const reader = new FileReader();
        reader.onload = () => {
          this.campaignImage = reader.result as string;
        };
        reader.readAsDataURL(apiService);
      }
    )
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
                this.router.navigate(['/home'])
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