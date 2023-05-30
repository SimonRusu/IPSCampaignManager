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

  metricParams: string[] = ["manhattan", "chebyshev", "minkowski"]
  algorithParams: string[] = ["brute", "ball_tree", "kd_tree", "auto"]
  kernelParams: string[] = ["linear", "poly", "rbf", "sigmoid", "laplacian", "exponential", "linear_constant"]
  gammaParams: string[] = ["auto", "scale", "range"]
  WKNNparams: boolean = false;
  SVRparams: boolean = false;
  NuSVRparams: boolean = false;
  LinearSVRparams: boolean = false;
  SVRgammaRange: boolean = false;
  NuSVRgammaRange: boolean = false;


  seleccionada: string = this.methods[0];
  form!: FormGroup;


  constructor(
    private apiService: ApiService, private formBuilder: FormBuilder, private toastr: ToastrService, private router: Router){}
  
    ngOnInit(){
      this.apiService.getCampaignImagesById(this.campaign.Id).subscribe((response: Blob) => {
        if(response != null){
        const zipImages = new JSZip();
        zipImages.loadAsync(response).then(images =>{
          Object.keys(images.files).forEach(filename => {
            images.files[filename].async('base64').then(imageData => {
              const imageUrl = 'data:image/jpeg;base64,' + imageData;
              this.campaignImages.push(imageUrl);
            })
          })
        })
      }
      })
      
      this.form = this.formBuilder.group({
        methods: ['', Validators.required],
        protocols: ['', Validators.required],
        channels: ['', Validators.required],
        sample: ['', Validators.required],
        metric: ['', Validators.required],
        algorithm: ['', Validators.required],
        kernel: ['', Validators.required],
        cStep: ['', Validators.required],
        iStep: ['', Validators.required],
        gStep: ['', Validators.required],
        nuStep: ['', Validators.required],
        gamma: ['', Validators.required],
        kRangeStart: [1],
        kRangeEnd: [10],
        cRangeStart: [0.1],
        cRangeEnd: [20],
        gRangeStart: [0.01],
        gRangeEnd: [1],
        nuRangeStart: [0.01],
        nuRangeEnd: [1],
        iRangeStart: [1],
        iRangeEnd: [10000]
      });
    }

    formatLabel(value: number): string {
      if (value >= 1000) {
        return Math.round(value / 1000) + 'k';
      }
  
      return `${value}`;
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

    onMethodSelected(method: string){
        this.validateAndClearFields();

        this.WKNNparams = false;
        this.SVRparams = false;
        this.NuSVRparams = false;
        this.LinearSVRparams = false;
        this.SVRgammaRange = false;
        this.NuSVRgammaRange = false;
    
        switch(method){
          case "WKNN":
            this.WKNNparams = true;
            this.form.get('cStep')?.setValidators(null);
            this.form.get('nuStep')?.setValidators(null);
            this.form.get('iStep')?.setValidators(null);
            this.form.get('gStep')?.setValidators(null);
            this.form.get('gamma')?.setValidators(null);
            this.form.get('kernel')?.setValidators(null);
            break;
          case "SVR":
            this.SVRparams = true;
            this.form.get('algorithm')?.setValidators(null);
            this.form.get('metric')?.setValidators(null);
            this.form.get('iStep')?.setValidators(null);
            this.form.get('nuStep')?.setValidators(null);
            this.form.get('gStep')?.setValidators(null);
            break;
          case "NuSVR":
            this.NuSVRparams = true;
            this.form.get('algorithm')?.setValidators(null);
            this.form.get('metric')?.setValidators(null);
            this.form.get('iStep')?.setValidators(null);
            this.form.get('gStep')?.setValidators(null);
            break;
          case "LinearSVR":
            this.LinearSVRparams = true;
            this.form.get('algorithm')?.setValidators(null);
            this.form.get('metric')?.setValidators(null);
            this.form.get('gStep')?.setValidators(null);
            this.form.get('nuStep')?.setValidators(null);
            break;
        }
        
        Object.keys(this.form?.controls).forEach(key => {
          this.form?.get(key)?.updateValueAndValidity();
        });
    }

    onSVRGammaSelected(gamma: string){
        this.SVRgammaRange = false;

        if(gamma === "range"){
          this.SVRgammaRange = true;
          this.form.get('gStep')?.setValidators(Validators.required);
        }
        this.form?.get('gStep')?.updateValueAndValidity();
    }

    onNuSVRgammaSelected(gamma: string){
        this.NuSVRgammaRange = false;

        if(gamma === "range"){
          this.NuSVRgammaRange = true;
          this.form.get('gStep')?.setValidators(Validators.required);
        }
        this.form?.get('gStep')?.updateValueAndValidity();
    }

    validateAndClearFields(){
      this.form.get('methods')?.setValidators(Validators.required);
      this.form.get('protocols')?.setValidators(Validators.required);
      this.form.get('channels')?.setValidators(Validators.required);
      this.form.get('sample')?.setValidators(Validators.required);
      this.form.get('metric')?.setValidators(Validators.required);
      this.form.get('metric')?.reset();
      this.form.get('algorithm')?.setValidators(Validators.required);
      this.form.get('algorithm')?.reset();
      this.form.get('cStep')?.setValidators(Validators.required);
      this.form.get('cStep')?.reset();
      this.form.get('nuStep')?.setValidators(Validators.required);
      this.form.get('nuStep')?.reset();
      this.form.get('iStep')?.setValidators(Validators.required);
      this.form.get('iStep')?.reset();
      this.form.get('gStep')?.setValidators(Validators.required);
      this.form.get('gStep')?.reset();
      this.form.get('gamma')?.setValidators(Validators.required);
      this.form.get('gamma')?.reset();
      this.form.get('kernel')?.setValidators(Validators.required);
      this.form.get('kernel')?.reset();
    }

    applyMethod(){
      let formData = new FormData();
      let campaignId = this.campaign.Id;
      let campaignName = this.campaign.Name;
      let selectedMethods = this.form.get('methods')?.value;
      let selectedProtocols = this.form.get('protocols')?.value;
      let selectedChannels = this.form.get('channels')?.value;
      let selectedSample = this.form.get('sample')?.value;
      let kRangeStart = this.form.get('kRangeStart')?.value;
      let kRangeEnd = this.form.get('kRangeEnd')?.value;

      selectedChannels= selectedChannels.map((channel: string) => parseInt(channel));

      let dataPackage = {
        campaign: campaignId,
        campaignName: campaignName,
        methods: selectedMethods,
        protocols: selectedProtocols,
        channels: selectedChannels,
        sample: selectedSample,
        kRangeStart: kRangeStart,
        kRangeEnd: kRangeEnd,
      };
      
      formData.append('params', JSON.stringify(dataPackage));
      
      this.toastr.clear();
      this.toastr.warning('Conectando con el servidor...', 'Operación en curso', { timeOut: 2000 });

      this.apiService.applyMethod(formData).pipe(
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
