import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-history-item-card',
  templateUrl: './history-item-card.component.html',
  styleUrls: ['./history-item-card.component.sass']
})
export class HistoryItemCardComponent {
  @Input() task!: any;
}
