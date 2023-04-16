import { Component } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { ApiService } from '../services/api.service';



@Component({
  selector: 'app-upload-campaign',
  templateUrl: './upload-campaign.component.html',
  styleUrls: ['./upload-campaign.component.sass']
})
export class UploadCampaignComponent {

  uploadForm: FormGroup;

  constructor(
    private toastr: ToastrService, 
    private fb: FormBuilder, 
    private apiService: ApiService)
  {
    this.uploadForm = this.fb.group({
      name: ['', [Validators.required]],
      date: [new Date().toISOString().substring(0, 10), Validators.required],
      description: []
    });
  }
  
  firstSelectedFile: File | null = null;
  secondSelectedFile: File | null = null;
  selectedImages: File[] = [];
  firstFileUploaded = false;
  secondFileUploaded = false;
  imageUploaded = false;
  fileNames: string[] = [];
  imageNames: string[] = [];
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

  onSelected(event: any, type: string) {
    this.onSelectedOrOnDrop(event.target.files, type);
  }

  onDrop(event: any, type: string) {
    event.preventDefault();
    this.onSelectedOrOnDrop(event.dataTransfer.files, type);
  }
  
  onSelectedOrOnDrop(files: any, type: string) {
    if(type == 'image'){
      this.isDraggingImage = false;
      for(let i = 0; i < files.length; i++){
        var file = files[i];
     
        if (!this.imageAllowedExtensions.includes(file.type)) {
          this.toastr.error('El archivo no posee un formato válido (JPEG, JPG, PNG, GIF)', 'Error de formato');
        }
        else{
          this.imageUploaded = true;
          this.selectedImages?.push(file);
          this.imageNames?.push(file.name);
        }
      }
    } else{
      this.isDraggingFile = false;
      if (files.length === 1) {
        var checkFile = files[0];
       

        if (checkFile && !this.fileAllowedExtensions.exec(checkFile.name)) {
          this.toastr.error('El archivo no posee un formato válido (SQLITE3)', 'Error de formato');
          return
        } 
        else {
          if (this.secondSelectedFile != null)
            this.firstSelectedFile = this.secondSelectedFile;

          this.secondSelectedFile = checkFile;

          if (this.secondSelectedFile?.name) {

            if(this.fileNames[0] == null){

              this.firstFileUploaded = true;
              this.fileNames[0] = this.secondSelectedFile?.name
            }
            else{
              this.secondFileUploaded = true;
              if(this.firstSelectedFile){
                this.fileNames[0] = this.firstSelectedFile?.name;
                this.fileNames[1] = this.secondSelectedFile?.name;
              }
            }
          }
        }
      }
      else if(files.length == 2){
        var checkFile = files[0];
        var checkFile2 = files[1];

        if (checkFile && !this.fileAllowedExtensions.exec(checkFile.name)) {
          this.toastr.error('El archivo no posee un formato válido (SQLITE3)', 'Error de formato');
          return;
        }
        else{
          this.firstSelectedFile = checkFile;
          this.firstFileUploaded = true;
          if (this.firstSelectedFile?.name) {
            this.fileNames[0] = this.firstSelectedFile?.name;
          }
        }

        if (checkFile2 && !this.fileAllowedExtensions.exec(checkFile2.name)) {
          this.toastr.error('El archivo no posee un formato válido (SQLITE3)', 'Error de formato');
          return;
        }
        else{
          this.secondSelectedFile = checkFile2;
          this.secondFileUploaded = true;
          if (this.secondSelectedFile?.name) {
            this.fileNames[1] = this.secondSelectedFile?.name;
          }

        }
      }
      else
        this.toastr.error('Solo se permite cargar dos ficheros de forma simultánea', 'Limite de ficheros excedido');
        return;
    } 
  }

  uploadCampaign(): void {
    const formData = new FormData();

    formData.append('name', this.uploadForm.get('name')?.value);
    formData.append('date', this.uploadForm.get('date')?.value);
    formData.append('description', this.uploadForm.get('description')?.value);

    if (this.selectedImages) {
      for (let i = 0; i < this.selectedImages.length; i++) {
        formData.append('images', this.selectedImages[i]);
      }
    }
    
    if (this.firstSelectedFile && this.secondSelectedFile) {
 
      formData.append('files', this.firstSelectedFile);
      formData.append('files', this.secondSelectedFile);
    }

    this.toastr.warning('Conectando con el servidor...', 'Operación en curso');
    this.apiService.uploadCampaign(formData).subscribe();
  }
}