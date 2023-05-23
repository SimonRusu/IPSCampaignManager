import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HistoryItemCardComponent } from './history-item-card.component';

describe('HistoryItemCardComponent', () => {
  let component: HistoryItemCardComponent;
  let fixture: ComponentFixture<HistoryItemCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HistoryItemCardComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HistoryItemCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
