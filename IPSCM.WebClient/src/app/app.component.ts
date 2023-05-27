import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent {
  title = 'IPSCM.WebClient';

  constructor(private router: Router) { }

  ngOnInit() {
    this.router.navigateByUrl('/campaigns');
  }
}


