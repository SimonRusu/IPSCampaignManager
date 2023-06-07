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
  campaignMethodPrediction: any = [];
  campaignId: any;
  methods: string[] = ["WKNN", "SVR", "NuSVR", "LinearSVR"];
  selectAllMethodsCheck: boolean = false;
  form!: FormGroup;

  ngOnInit(){
    this.form = this.formBuilder.group({
      methods: ['', Validators.required]
    });
  }

  
  constructor(private route: ActivatedRoute, private apiService: ApiService, private formBuilder: FormBuilder){
    this.route.queryParams.subscribe(params => {
      if(params['data']){
        this.campaignId = params['data'];
        console.log(this.campaignId)
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
    console.log(allMethods)
    
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

  onMethodSelected(method: string){
    console.log(method)
  }
  
  public lineChartData: ChartConfiguration['data'] = {
    datasets: [
      {
        data: [ 65, 59, 80, 81, 56, 55, 40 ],
        label: 'Series A',
        backgroundColor: 'rgba(148,159,177,0.2)',
        borderColor: 'rgba(148,159,177,1)',
        pointBackgroundColor: 'rgba(148,159,177,1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(148,159,177,0.8)',
        fill: 'origin',
      },
      {
        data: [ 28, 48, 40, 19, 86, 27, 90 ],
        label: 'Series B',
        backgroundColor: 'rgba(77,83,96,0.2)',
        borderColor: 'rgba(77,83,96,1)',
        pointBackgroundColor: 'rgba(77,83,96,1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(77,83,96,1)',
        fill: 'origin',
      },
      {
        data: [ 180, 480, 770, 90, 1000, 270, 400 ],
        label: 'Series C',
        yAxisID: 'y1',
        backgroundColor: 'rgba(255,0,0,0.3)',
        borderColor: 'red',
        pointBackgroundColor: 'rgba(148,159,177,1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(148,159,177,0.8)',
        fill: 'origin',
      }
    ],
    labels: [ 'January', 'February', 'March', 'April', 'May', 'June', 'July' ]
  };

  public lineChartOptions: ChartConfiguration['options'] = {
    elements: {
      line: {
        tension: 0.5
      }
    },
    scales: {
      // We use this empty structure as a placeholder for dynamic theming.
      y:
        {
          position: 'left',
        },
      y1: {
        position: 'right',
        grid: {
          color: 'rgba(255,0,0,0.3)',
        },
        ticks: {
          color: 'red'
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
