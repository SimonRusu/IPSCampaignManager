import { Component, ElementRef, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Chart, ChartConfiguration, ChartData, ChartEvent, ChartType } from 'chart.js';
import { ApiService } from '../services/api.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import annotationPlugin from 'chartjs-plugin-annotation';


@Component({
  selector: 'app-graphics',
  templateUrl: './graphics.component.html',
  styleUrls: ['./graphics.component.sass']
})
export class GraphicsComponent {

  @ViewChild('chartCanvas', { static: true }) chartCanvas!: ElementRef<HTMLCanvasElement>;
  campaignId: any;
  campaignMethodPrediction: any = [];
  filteredData: any = [];
  campaignFilteredPoints: any = [];
  campaoignFilteredErrors: any = [];
  methods: string[] = ["WKNN", "SVR", "NuSVR", "LinearSVR"];
  protocols: string[] = ["Eddystone", "iBeacon"];
  channels: string[] = ["37", "38", "39"];
  selectAllMethodsCheck: boolean = false;
  selectAllProtocolsCheck: boolean = false;
  selectAllChannelsCheck: boolean = false;
  form!: FormGroup;

  ngOnInit(){
    this.form = this.formBuilder.group({
      methods: ['', Validators.required],
      protocols: ['', Validators.required],
      channels: ['', Validators.required]
    });

    Chart.register(annotationPlugin);
  }

  
  constructor(private route: ActivatedRoute, private apiService: ApiService, private formBuilder: FormBuilder){
    this.route.queryParams.subscribe(params => {
      if(params['data']){
        this.campaignId = params['data'];
      }
    })

    this.apiService.getMethodPredictionsById(this.campaignId).subscribe(res=> {
      
      if(res != 0){
        this.campaignMethodPrediction = res
      }
    })
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
      this.onFilterSelected();
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
      this.onFilterSelected();
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
      this.onFilterSelected();
    }
  }

  onFilterSelected(){
    this.filteredData = [...this.campaignMethodPrediction];

    this.filteredData = this.filterData(this.form.get('methods')?.value, "method", this.filteredData);
    this.filteredData = this.filterData(this.form.get('protocols')?.value, "protocol", this.filteredData);
    this.filteredData = this.filterData(this.form.get('channels')?.value, "channel", this.filteredData);

    let sortedData = this.parseData()
    this.fillPrecisionData(sortedData)
  }

  filterData(filters: any, property: string, data: any[]): any[]{
    return data.filter((object:any) =>{
      const methodDescription = JSON.parse(object.Method_description);
      return filters.some((filter: string) => filter === methodDescription[property].toString());
    })
  }
  
  parseData() {
    let parsedData = this.filteredData.map((item:any) => {
        let meanErrors = JSON.parse(item.Mean_error);
      
        let sortedData = Object.keys(meanErrors).map(key => ({
            key: key,
            meanError: meanErrors[key]
        }
        ));
      
        const cdfValues = this.calculateCDF(sortedData);

        return {
            ...item,
            SortedData: sortedData,
            CdfValues: cdfValues
        };
    });

    return parsedData;
  }

  calculateCDF(sortedData: any) {
    const cdfData = [];

    for (let i = 0; i < sortedData.length; i++) {
        let meanErrors = sortedData[i].meanError;
        let cdf:any = [];
        let totalCount = meanErrors.length;
        let cumulativeCount = 0;

        meanErrors.forEach((errorValue:any, index:any) => {
            cumulativeCount += 1;
            const probability = cumulativeCount / totalCount;
            cdf.push({ x: errorValue, y: probability });
        });

        cdfData.push({
            key: sortedData[i].key,
            cdf: cdf
        });
    }

    return cdfData;
}
  

  fillPrecisionData(filteredData:any){
    let labels = [];
    let datasets = [];
    for(let i = 0; i < filteredData.length; i++){
      let item = filteredData[i];
      let cdfValues = item.CdfValues;

      for(let j = 0; j < cdfValues.length; j++){
          let data = cdfValues[j];
          console.log(data)
          let meanErrors = data.cdf;
          
          let hue = Math.floor(((i * cdfValues.length + j) * 360) / (filteredData.length * cdfValues.length));
          let color = `hsl(${hue}, 100%, 50%)`;
          let backgroundColor = `hsla(${hue}, 100%, 50%, 0.2)`;

          
          let dataset = {
              data: meanErrors,
              label: data.key,
              backgroundColor: backgroundColor,
              borderColor: color,
              pointBackgroundColor: color,
              pointBorderColor: '#fff',
              pointHoverBackgroundColor: '#fff',
              pointHoverBorderColor: color,
              fill: 'origin',
              hidden: true
          }
          datasets.push(dataset);
          labels.push(...meanErrors);
      }
  }

    this.lineChartData = {
      datasets: datasets,
      labels: labels
    };

  }
  
  public lineChartData: ChartConfiguration['data'] = {
    datasets: [],
    labels: []
  };

  public lineChartOptions: ChartConfiguration['options'] = {
    maintainAspectRatio:false,
    scales: {
      x: {
          title: {
              display: true,
              text: 'Error (m)'
          },
          beginAtZero: true,
          type:"linear",
          max: 10,
          ticks: {
            stepSize: 2,
          },
      },
      y: {
          title: {
              display: true,
              text: 'Distribución acumulada (CDF)'
          },
          type:"linear",
          min: 0,
          max: 1
      },
    },
    plugins:{
      legend:{
        display:true,
        position:"bottom",
        labels:{
          boxWidth:0.1,
          boxHeight:0.1,
        }
        
      }
    },
  };

  public lineChartType: ChartType = 'line';
  public radarChartOptions: ChartConfiguration['options'] = {
    responsive: true,
  };
  public radarChartLabels: string[] = [ 'Eating', 'Drinking', 'Sleeping', 'Designing', 'Coding', 'Cycling', 'Running' ];

  public radarChartData: ChartData<'radar'> = {
    labels: this.radarChartLabels,
    datasets: [
      { data: [ 65, 59, 90, 81, 56, 55, 40 ], label: 'Series A' },
      { data: [ 28, 48, 40, 19, 96, 27, 100 ], label: 'Series B' }
    ]
  };
  public radarChartType: ChartType = 'radar';

}