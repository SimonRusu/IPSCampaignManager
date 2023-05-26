import { Component, Input, ViewChild, ChangeDetectorRef } from '@angular/core';
import { ApiService } from '../services/api.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';

@Component({
  selector: 'app-task-history',
  templateUrl: './task-history.component.html',
  styleUrls: ['./task-history.component.sass']
})
export class TaskHistoryComponent {
  @Input() task!: any;
  @ViewChild('historyItemPaginator', { static: false }) set content(paginator: MatPaginator) {
    if(paginator) { 
      this.historyItemDataSource.paginator = paginator;
      paginator.length = this.historyTasks.length;
      this.cdr.detectChanges();
    }
  }

  historyItemColumns = ['Name', 'Status', 'Task_description', 'Datetime_start', 'Datetime_end']
  historyItemColumnsSpa = ['Campaña', 'Estado', 'Descripción de la tarea', 'Fecha de inicio', 'Fecha de fin'];
  historyTasks: any = [];
  historyItemDataSource = new MatTableDataSource<any>([]);
  pageSizes = [10, 25, 50, 100];
  defaultPageSize = 10;

  constructor(private apiService: ApiService, private cdr: ChangeDetectorRef) { }
  ngOnInit(){
    this.apiService.pollTaskHistory().subscribe(data => {
      const objectsArray: any[] = [...Object.values(data)];
      this.historyItemDataSource.data = objectsArray;
      this.historyTasks = objectsArray;
    });
  }

  getColumnName(column: string): string {
    const index = this.historyItemColumns.indexOf(column);
    return this.historyItemColumnsSpa[index];
  }
}
