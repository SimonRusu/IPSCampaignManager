import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, map, of, tap } from 'rxjs';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = 'http://localhost:5000/api/';

  constructor(private http: HttpClient, 
    private toastr: ToastrService,
    private router: Router) {}

  getCampaigns(){
    return this.http.get(this.baseUrl+ "campaigns");
  }

  getCampaignImageById(id: any): Observable<any> {
    return this.http.get(this.baseUrl + `campaignImage/${id}`, { responseType: 'blob' })
    .pipe(
      map(response => {
        return response;
      })
    );
  }

  deleteCampaignById(id: any) {
    return this.http.delete(this.baseUrl + `deleteCampaign/${id}`);
  }

  uploadCampaign(formData: FormData): Observable<any> {
    return this.http.post(this.baseUrl + 'upload_campaign', formData).pipe(
    tap(() => {
        this.toastr.success('¡La campaña se ha guardado correctamente!', 'Operación completada');
        this.router.navigate(['/home']);
      }),
      catchError(() => {
        this.toastr.error('Ha ocurrido un error durante la operación', 'Operación no completada');
        return of(null);
      })
    );
  }
  
}
