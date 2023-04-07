import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadCampaignComponent } from './upload-campaign.component';

describe('UploadCampaignComponent', () => {
  let component: UploadCampaignComponent;
  let fixture: ComponentFixture<UploadCampaignComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UploadCampaignComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UploadCampaignComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
