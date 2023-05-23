import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = 'http://localhost:5000/api/';

  constructor(private http: HttpClient) {}

  getCampaigns(){
    return this.http.get(this.baseUrl + "campaigns");
  }

  getTaskHistory(){
    return this.http.get(this.baseUrl + "taskHistory");
  }

  getRelatedCampaignById(id: any){
    return this.http.get(this.baseUrl + `relatedCampaign/${id}`);
  }

  getCampaignImagesById(id: any): Observable<any> {
    return this.http.get(this.baseUrl + `campaignImages/${id}`, { responseType: 'blob' })
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
    return this.http.post(this.baseUrl + 'upload_campaign', formData);
  }

  deleteCampaignById(id: any){
    return this.http.delete(this.baseUrl + `deleteCampaign/${id}`);
  }
}