import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { ToastrService } from 'ngx-toastr';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../services/api.service';



@Component({
  selector: 'app-upload-campaign',
  templateUrl: './upload-campaign.component.html',
  styleUrls: ['./upload-campaign.component.sass']
})
export class UploadCampaignComponent {

  uploadForm: FormGroup;

  constructor(private http: HttpClient,
    private toastr: ToastrService, 
    private fb: FormBuilder, 
    private router: Router, 
    private apiService: ApiService)
  {
    this.uploadForm = this.fb.group({
      name: ['', [Validators.required]],
      date: [new Date().toISOString().substring(0, 10), Validators.required],
      description: []
    });
  }
  
  selectedFile: File | null = null;
  selectedImage: File | null = null;
  fileUploaded = false;
  imageUploaded = false;
  fileName: string | undefined;
  imageName: string | undefined;
  isDraggingFile = false;
  isDraggingImage = false;
  fileAllowedExtensions = /(\.sqlite3)$/i;
  imageAllowedExtensions = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];

  onDragOver(event: any, type: string){
    event.preventDefault();
    event.stopPropagation();

    if(type == 'image'){
      this.isDraggingImage = true;
    }
    else this.isDraggingFile = true;
  }

  onDragLeave(event: any, type: string){
    event.preventDefault();
    event.stopPropagation();
    
    if(type == 'image'){
      this.isDraggingImage = false;
    }
    else this.isDraggingFile = false;
  }

  onDrop(event: any, type: string){
    event.preventDefault();
    event.stopPropagation();

    const file = event.dataTransfer.files[0];

    if(type == 'image'){
      this.selectedImage = file;
      this.isDraggingImage = false;

      if (this.selectedImage && !this.imageAllowedExtensions.includes(this.selectedImage.type)) {
        this.toastr.error('El archivo no posee un formato válido (JPEG, JPG, PNG, GIF)', 'Error de formato');
        this.imageName = "No hay ningún archivo cargado"
        this.imageUploaded = false;
        return;
      }
      
      this.imageUploaded = true;
      this.imageName = this.selectedImage?.name;
    }
    else{
      this.selectedFile = file;
      this.isDraggingFile = false;

      if (this.selectedFile && !this.fileAllowedExtensions.exec(this.selectedFile.name)) {
        this.toastr.error('El archivo no posee un formato válido (SQLITE3)', 'Error de formato');
        this.fileName = "No hay ningún archivo cargado"
        this.fileUploaded = false;
        return;
      }
      
      this.fileUploaded = true;
      this.fileName = this.selectedFile?.name;
    } 
  }
  
  onSelected(event: any, type: string) {
    const file = event.target.files[0];

    if(type == "image"){
      this.selectedImage = file;

      if (this.selectedImage && !this.imageAllowedExtensions.includes(this.selectedImage.type)) {
        this.toastr.error('El archivo no posee un formato válido (JPEG, JPG, PNG, GIF)', 'Error de formato');
        this.imageName = "No hay ningún archivo cargado"
        this.imageUploaded = false;
        return;
      }
        
        this.imageName = this.selectedImage?.name;
        this.imageUploaded = this.imageName ? true : false;


    } else{
      this.selectedFile = file;

      if (this.selectedFile && !this.fileAllowedExtensions.exec(this.selectedFile.name)) {
        this.toastr.error('El archivo no posee un formato válido (SQLITE3)', 'Error de formato');
        this.fileName = "No hay ningún archivo cargado"
        this.fileUploaded = false;
        return;
      }

        this.fileName = this.selectedFile?.name;
        this.fileUploaded = this.fileName ? true : false;
    }
  }

  uploadCampaign(): void {
    const formData = new FormData();

    formData.append('name', this.uploadForm.get('name')?.value);
    formData.append('date', this.uploadForm.get('date')?.value);
    formData.append('description', this.uploadForm.get('description')?.value);

    if (this.selectedImage) {
      formData.append('image', this.selectedImage);
    }

    if (this.selectedFile) {
      formData.append('file', this.selectedFile);
    }

    this.toastr.warning('Conectando con el servidor...', 'Operación en curso');
    this.apiService.uploadCampaign(formData).subscribe();
  }
}
