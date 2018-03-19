import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Social Media Influence Ranker';
  msg = ""
  Login() {
    this.msg = "clicked"
  }
}