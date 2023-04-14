import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IpsCampaignCardComponent } from './ips-campaign-card.component';

describe('IpsCampaignCardComponent', () => {
  let component: IpsCampaignCardComponent;
  let fixture: ComponentFixture<IpsCampaignCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IpsCampaignCardComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IpsCampaignCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
