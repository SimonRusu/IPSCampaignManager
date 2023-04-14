import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IpsMethodsComponent } from './ips-methods.component';

describe('IpsMethodsComponent', () => {
  let component: IpsMethodsComponent;
  let fixture: ComponentFixture<IpsMethodsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IpsMethodsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IpsMethodsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
