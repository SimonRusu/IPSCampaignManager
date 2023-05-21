import { Component, Input } from '@angular/core';
import { ApiService } from '../services/api.service';
import JSZip from 'jszip';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { catchError, of, tap } from 'rxjs';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router';


@Component({
  selector: 'app-ips-campaign-card',
  templateUrl: './ips-campaign-card.component.html',
  styleUrls: ['./ips-campaign-card.component.sass']
})


export class IpsCampaignCardComponent {
  @Input() campaign!: any;
  campaignImages: string[] = [];
  methods: string[] = ["WKNN", "SVR", "NuSVR", "LinearSVR"];
  protocols: string[] = ["Eddystone", "iBeacon"];
  channels: string[] = ["37", "38", "39"];
  samples = Array.from({length: 20}, (_, index) => index + 1);
  selectAllMethodsCheck: boolean = false;
  selectAllProtocolsCheck: boolean = false;
  selectAllChannelsCheck: boolean = false;


  seleccionada: string = this.methods[0];
  form!: FormGroup;


  constructor(
    private apiService: ApiService, private formBuilder: FormBuilder, private toastr: ToastrService, private router: Router ){}
  
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
      
      this.form = this.formBuilder.group({
        methods: ['', Validators.required],
        protocols: ['', Validators.required],
        channels: ['', Validators.required],
        sample: ['', Validators.required],
        kRangeStart: [1],
        kRangeEnd: [10],
      });
    }

    formatLabel(value: number): string {
      if (value >= 1000) {
        return Math.round(value / 1000) + 'k';
      }
  
      return `${value}`;
    }

    selectAllMethods(){
      const methodsControl = this.form.get('methods');
      const methodsToggle = this.form.get('methods')?.value;

      const allMethods = this.methods.slice();
      
      if(methodsControl){
        if (methodsToggle.length == 1) {
          methodsControl.setValue(allMethods);
          this.selectAllMethodsCheck = true;
        } else {
          methodsControl.setValue([]);
          this.selectAllMethodsCheck = false;
        }
      }
    }

    selectAllProtocols(){
      const protocolsControl = this.form.get('protocols');
      const protocolsToggle = this.form.get('protocols')?.value;

      const allProtocols = this.protocols.slice();
      
      if(protocolsControl){
        if (protocolsToggle.length == 1) {
          protocolsControl.setValue(allProtocols);
          this.selectAllProtocolsCheck = true;
        } else {
          protocolsControl.setValue([]);
          this.selectAllProtocolsCheck = false;
        }
      }
    }

    selectAllChannels(){
      const channelsControl = this.form.get('channels');
      const channelsToggle = this.form.get('channels')?.value;

      const allChannels = this.channels.slice();
      
      if(channelsControl){
        if (channelsToggle.length == 1) {
          console.log(channelsToggle)
          channelsControl.setValue(allChannels);
          this.selectAllChannelsCheck = true;
        } else {
          channelsControl.setValue([]);
          this.selectAllChannelsCheck = false;
        }
      }
    }

    applyMethod(){
      let formData = new FormData();
      let campaignId = this.campaign.Id;
      let selectedMethods = this.form.get('methods')?.value;
      let selectedProtocols = this.form.get('protocols')?.value;
      let selectedChannels = this.form.get('channels')?.value;
      let selectedSample = this.form.get('sample')?.value;
      let kRangeStart = this.form.get('kRangeStart')?.value;
      let kRangeEnd = this.form.get('kRangeEnd')?.value;

      selectedChannels= selectedChannels.map((channel: string) => parseInt(channel));

      let dataPackage = {
        campaign: campaignId,
        methods: selectedMethods,
        protocols: selectedProtocols,
        channels: selectedChannels,
        sample: selectedSample,
        kRangeStart: kRangeStart,
        kRangeEnd: kRangeEnd,
      };
      
      formData.append('params', JSON.stringify(dataPackage));

      this.apiService.applyMethod(formData).pipe(
        tap(response => {
          setTimeout(() => {
            this.toastr.clear();
            this.toastr.success('¡El método se ha aplicado correctamente!', 'Operación completada', { timeOut: 2000 });
            this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
              this.router.navigate(['/ips-methods'])
            });
          }, 0);
        }),
        catchError(error => {
          setTimeout(() => {
            this.toastr.clear();
            this.toastr.error('Ocurrió un error durante la aplicación del método', 'Operación no completada', { timeOut: 2000 });
          }, 0);
          return of(null);
        })
      ).subscribe();
  
    }


    
    


}
