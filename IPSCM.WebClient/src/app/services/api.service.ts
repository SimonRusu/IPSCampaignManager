import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { EMPTY, Observable, Subject, catchError, of, switchMap, takeUntil, throwError, timer } from 'rxjs';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = 'http://localhost:5000/api/';
  private destroy$ = new Subject();

  constructor(private http: HttpClient, private router: Router) {}

  getCampaigns(){
    return this.http.get(this.baseUrl + "campaigns");
  }

  getMethodPredictionsById(id: any){
    return this.http.get(this.baseUrl + `predictionsByCampaign/${id}`);
  }

  getTaskHistory(){
    return this.http.get(this.baseUrl + "taskHistory");
  }

  pollTaskHistory(): Observable<any> {
    return timer(0, 5000).pipe(
      takeUntil(this.destroy$),
      switchMap(() => {
        if (this.router.url === '/task-history') {
          return this.getTaskHistory();
        } else {
          this.destroy$.next(null);
          return EMPTY;
        }
      })
    );
  }

  getRelatedCampaignById(id: any){
    return this.http.get(this.baseUrl + `relatedCampaign/${id}`);
  }

  getCampaignImagesById(id: any): Observable<any> {
    return this.http.get(this.baseUrl + `campaignImages/${id}`, { responseType: 'blob' }).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 404) {
          return of(null);
        }
        return throwError(() => error);
      })
    );
  }

  getDongleName(id: any){
    return this.http.get(this.baseUrl + `dongleReceptor/${id}`);
  }

  getCampaignSequence(id: any){
    return this.http.get(this.baseUrl + `campaignSequence/${id}`);
  }

  getCaptures(id: any){
    return this.http.get(this.baseUrl + `capturesByCampaign/${id}`);
  }

  getSignals(id: any){
    return this.http.get(this.baseUrl + `signalsByCampaign/${id}`);
  }

  getConfigs(id: any){
    return this.http.get(this.baseUrl + `configsByCampaign/${id}`);
  }

  applyMethod(formData: FormData): Observable<any> {
    return this.http.post(this.baseUrl + 'applyMethod', formData);
  }

  uploadCampaign(formData: FormData): Observable<any> {
    return this.http.post(this.baseUrl + 'uploadCampaign', formData);
  }

  deleteCampaignById(id: any){
    return this.http.delete(this.baseUrl + `deleteCampaign/${id}`);
  }
}