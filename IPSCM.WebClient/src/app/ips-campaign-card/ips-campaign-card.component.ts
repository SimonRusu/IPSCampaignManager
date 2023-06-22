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
  selectAllProtocolsCheck: boolean = false;
  selectAllChannelsCheck: boolean = false;
  selectAllMetricsCheck: boolean = false;
  selectAllAlgorithmsCheck: boolean = false;

  metricParams: string[] = ["manhattan", "chebyshev", "minkowski"]
  algorithmParams: string[] = ["brute", "ball_tree", "kd_tree", "auto"]
  kernelParams: string[] = ["linear", "poly", "sigmoid", "rbf"]
  gammaParams: string[] = ["auto", "scale", "range"]
  WKNNparams: boolean = false;
  SVRparams: boolean = false;
  NuSVRparams: boolean = false;
  LinearSVRparams: boolean = false;
  SVRgammaRange: boolean = false;
  NuSVRgammaRange: boolean = false;


  selectedMethod: any;
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
        metrics: ['', Validators.required],
        algorithms: ['', Validators.required],
        kernels: ['', Validators.required],
        cStep: ['', Validators.required],
        iStep: ['', Validators.required],
        gStep: ['', Validators.required],
        nuStep: ['', Validators.required],
        gamma: ['', Validators.required],
        kRangeStart: [1],
        kRangeEnd: [20],
        cRangeStart: [0.1],
        cRangeEnd: [20],
        gRangeStart: [0.01],
        gRangeEnd: [1],
        nuRangeStart: [0.01],
        nuRangeEnd: [1],
        iRangeStart: [0],
        iRangeEnd: [10000]
      });
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
          channelsControl.setValue(allChannels);
          this.selectAllChannelsCheck = true;
        } else {
          channelsControl.setValue([]);
          this.selectAllChannelsCheck = false;
        }
      }
    }

    selectAllMetrics(){
      const metricsControl = this.form.get('metrics');
      const metricsToggle = this.form.get('metrics')?.value;

      const allMetrics = this.metricParams.slice();
      
      if(metricsControl){
        if (metricsToggle.length == 1) {
          metricsControl.setValue(allMetrics);
          this.selectAllMetricsCheck = true;
        } else {
          metricsControl.setValue([]);
          this.selectAllMetricsCheck = false;
        }
      }
    }

    selectAllAlgorithms(){
      const algorithmsControl = this.form.get('algorithms');
      const algorithmsToggle = this.form.get('algorithms')?.value;

      const allAlgorithms = this.algorithmParams.slice();
      
      if(algorithmsControl){
        if (algorithmsToggle.length == 1) {
          algorithmsControl.setValue(allAlgorithms);
          this.selectAllAlgorithmsCheck = true;
        } else {
          algorithmsControl.setValue([]);
          this.selectAllAlgorithmsCheck = false;
        }
      }
    }

    selectAllKernels(){
      const kernelsControl = this.form.get('kernels');
      const kernelsToggle = this.form.get('kernels')?.value;

      const allKernels = this.kernelParams.slice();
      
      if(kernelsControl){
        if (kernelsToggle.length == 1) {
          kernelsControl.setValue(allKernels);
          this.selectAllAlgorithmsCheck = true;
        } else {
          kernelsControl.setValue([]);
          this.selectAllAlgorithmsCheck = false;
        }
      }
    }

    onMethodSelected(method: string){
        this.selectedMethod = method;
        this.validateAndClearFields();
        this.WKNNparams = false;
        this.SVRparams = false;
        this.NuSVRparams = false;
        this.LinearSVRparams = false;
        this.SVRgammaRange = false;
        this.NuSVRgammaRange = false;
    
        switch(this.selectedMethod){
          case "WKNN":
            this.WKNNparams = true;
            this.form.get('cStep')?.setValidators(null);
            this.form.get('nuStep')?.setValidators(null);
            this.form.get('iStep')?.setValidators(null);
            this.form.get('gStep')?.setValidators(null);
            this.form.get('gamma')?.setValidators(null);
            this.form.get('kernels')?.setValidators(null);
            break;
          case "SVR":
            this.SVRparams = true;
            this.form.get('algorithms')?.setValidators(null);
            this.form.get('metrics')?.setValidators(null);
            this.form.get('iStep')?.setValidators(null);
            this.form.get('nuStep')?.setValidators(null);
            this.form.get('gStep')?.setValidators(null);
            break;
          case "NuSVR":
            this.NuSVRparams = true;
            this.form.get('algorithms')?.setValidators(null);
            this.form.get('metrics')?.setValidators(null);
            this.form.get('iStep')?.setValidators(null);
            this.form.get('gStep')?.setValidators(null);
            break;
          case "LinearSVR":
            this.LinearSVRparams = true;
            this.form.get('algorithms')?.setValidators(null);
            this.form.get('metrics')?.setValidators(null);
            this.form.get('gStep')?.setValidators(null);
            this.form.get('gamma')?.setValidators(null);
            this.form.get('nuStep')?.setValidators(null);
            this.form.get('kernels')?.setValidators(null);
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
      this.form.get('metrics')?.setValidators(Validators.required);
      this.form.get('metrics')?.reset();
      this.form.get('algorithms')?.setValidators(Validators.required);
      this.form.get('algorithms')?.reset();
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
      this.form.get('kernels')?.setValidators(Validators.required);
      this.form.get('kernels')?.reset();
    }

    applyMethodBtn(){
      let formData = new FormData();
      let campaignId = this.campaign.Id;
      let campaignName = this.campaign.Name;
      let selectedProtocols = this.form.get('protocols')?.value;
      let selectedChannels = this.form.get('channels')?.value;
      let selectedSample = this.form.get('sample')?.value;
      let metric;
      let algorithm;
      let kRangeStart;
      let kRangeEnd;
      let kernels;
      let cRangeStart;
      let cRangeEnd;
      let cStep;
      let gamma;
      let gRangeStart;
      let gRangeEnd;
      let gStep;
      let nuRangeStart;
      let nuRangeEnd;
      let nuStep;
      let iRangeStart;
      let iRangeEnd;
      let iStep;
      let cValues;
      let gValues;
      let nuValues;
      let iValues;
      
      selectedChannels= selectedChannels.map((channel: string) => parseInt(channel));

      let dataPackage = {
        campaign: campaignId,
        campaignName: campaignName,
        method: this.selectedMethod,
        protocols: selectedProtocols,
        channels: selectedChannels,
        sample: selectedSample,
        metrics: [0],
        algorithms: [0],
        kernels: [0],
        kRangeStart: 0,
        kRangeEnd: 0,
        gValues: [null],
        cValues: [null],
        nuValues: [null],
        iValues: [null]
      };

      switch(this.selectedMethod){

        case "WKNN":
            metric = this.form.get('metrics')?.value;
            algorithm = this.form.get('algorithms')?.value;
            kRangeStart = this.form.get('kRangeStart')?.value;
            kRangeEnd = this.form.get('kRangeEnd')?.value;

            dataPackage['metrics'] = metric;
            dataPackage['algorithms'] = algorithm;
            dataPackage['kRangeStart'] = kRangeStart;
            dataPackage['kRangeEnd'] = kRangeEnd;
            break;

          case "SVR":
            kernels = this.form.get('kernels')?.value;
            cRangeStart = this.form.get('cRangeStart')?.value;
            cRangeEnd = this.form.get('cRangeEnd')?.value;
            cStep = this.form.get('cStep')?.value;
            gamma = this.form.get('gamma')?.value;
            gRangeStart = this.form.get('gRangeStart')?.value;
            gRangeEnd = this.form.get('gRangeEnd')?.value;
            gStep = this.form.get('gStep')?.value;

            cValues = this.fillParamValues(cRangeStart, cRangeEnd, cStep);
            
            if (this.SVRgammaRange){
              gValues = this.fillParamValues(gRangeStart, gRangeEnd, gStep);
            }
            else gValues = gamma;

            dataPackage['kernels'] = kernels;
            dataPackage['cValues'] = cValues;
            dataPackage['gValues'] = gValues;
            break;

          case "NuSVR":
            kernels = this.form.get('kernels')?.value;
            cRangeStart = this.form.get('cRangeStart')?.value;
            cRangeEnd = this.form.get('cRangeEnd')?.value;
            cStep = this.form.get('cStep')?.value;
            gamma = this.form.get('gamma')?.value;
            gRangeStart = this.form.get('gRangeStart')?.value;
            gRangeEnd = this.form.get('gRangeEnd')?.value;
            gStep = this.form.get('gStep')?.value;
            nuRangeStart = this.form.get('nuRangeStart')?.value;
            nuRangeEnd = this.form.get('nuRangeEnd')?.value;
            nuStep = this.form.get('nuStep')?.value;

            cValues = this.fillParamValues(cRangeStart, cRangeEnd, cStep);
            nuValues = this.fillParamValues(nuRangeStart, nuRangeEnd, nuStep);
            
            if (this.NuSVRgammaRange){
              gValues = this.fillParamValues(gRangeStart, gRangeEnd, gStep);
            }
            else gValues = gamma;

            dataPackage['kernels'] = kernels;
            dataPackage['cValues'] = cValues;
            dataPackage['gValues'] = gValues;
            dataPackage['nuValues'] = nuValues;
            break;

          case "LinearSVR":
            cRangeStart = this.form.get('cRangeStart')?.value;
            cRangeEnd = this.form.get('cRangeEnd')?.value;
            cStep = this.form.get('cStep')?.value;
            iRangeStart = this.form.get('iRangeStart')?.value;
            iRangeEnd = this.form.get('iRangeEnd')?.value;
            iStep = this.form.get('iStep')?.value;

            cValues = this.fillParamValues(cRangeStart, cRangeEnd, cStep);
            iValues = this.fillParamValues(iRangeStart, iRangeEnd, iStep);

            dataPackage['cValues'] = cValues;
            dataPackage['iValues'] = iValues;
            break;
      }


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

    fillParamValues(start:any, end:any, step:any){
      const result: any[] = [];

      while (start <= end) {
        result.push(Number(start.toFixed(2)));
        start += step;
      }
      return result;
    }
}
