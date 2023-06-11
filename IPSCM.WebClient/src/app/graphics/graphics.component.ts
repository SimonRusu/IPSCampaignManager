import { Component, ElementRef, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Chart, ChartConfiguration, ChartData, ChartEvent, ChartType } from 'chart.js';
import { ApiService } from '../services/api.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';


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
        this.filteredData = res
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

    let sortedData = this.sortData()
    this.fillPrecisionData(sortedData)
  }

  filterData(filters: any, property: string, data: any[]): any[]{
    return data.filter((object:any) =>{
      const methodDescription = JSON.parse(object.Method_description);
      return filters.some((filter: string) => filter === methodDescription[property].toString());
    })
  }
  
  sortData() {
    let parsedData = this.filteredData.map((item:any) => {
        let predictedPoints = JSON.parse(item.Predicted_points);
        let meanErrors = JSON.parse(item.Mean_error);
      
        let sortedData = Object.keys(predictedPoints).map(key => ({
            key: key,
            predictedPoint: predictedPoints[key],
            meanError: meanErrors[key]
        }));
      
        sortedData.sort((a, b) => a.meanError - b.meanError);
        let cdfValues = sortedData.map((value, i) => ((i + 1) / sortedData.length) * 100);
      
        return {
            ...item,
            SortedData: sortedData,
            CdfValues: cdfValues
        };
    });

    return parsedData;
  }

  fillPrecisionData(filteredData:any){
    let labels = [];
    let datasets = [];

    for(let i = 0; i < filteredData.length; i++){
      let item = filteredData[i];
      let sortedData = item.SortedData;
      let meanErrors = [];
      let cdfValues = item.CdfValues;

      for(let data of sortedData){
        meanErrors.push(data.meanError);
      }

      let hue = Math.floor((i * 360) / filteredData.length);
      let color = `hsl(${hue}, 100%, 50%)`;
      let backgroundColor = `hsla(${hue}, 100%, 50%, 0.2)`;


      let dataset = {
        data: cdfValues,
        label: `Series ${item.Id}`,
        backgroundColor: backgroundColor,
        borderColor: color,
        pointBackgroundColor: color,
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: color,
        fill: 'origin',
      }

      datasets.push(dataset);
      labels = meanErrors;
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
    scales: {
      xAxis: {
          title: {
              display: true,
              text: 'Error (m)'
          },
          beginAtZero: true,
          type:"linear",
          min: 0,
          max: 10,
          ticks: {
            stepSize: 2,
            
          }
      },
      y: {
          title: {
              display: true,
              text: 'Distribución acumulada (CDF)'
          },
          type:"linear",
          min: 0,
          max: 100
      }
    }
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
