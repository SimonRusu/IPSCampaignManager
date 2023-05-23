import { Component } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-task-history',
  templateUrl: './task-history.component.html',
  styleUrls: ['./task-history.component.sass']
})
export class TaskHistoryComponent {
  historyTasks: any = [];
  p: number = 1;

  constructor(private apiService: ApiService){

  }

  ngOnInit(){
    this.apiService.getTaskHistory().subscribe(data => {
      console.log(data)
      this.historyTasks = data;
    });
  }
}
