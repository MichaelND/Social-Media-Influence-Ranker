'use strict';

$(document).ready(function(){
	$('.tabs').tabs();
});
angular.module('recommenderApp', ['ui.router', 'ngDialog', 'ngResource', 'ngSanitize', 'recommenderApp.services'])
.config(function($httpProvider) {
	$httpProvider.useApplyAsync(true);
})
.config(function($stateProvider, $urlRouterProvider) {
	$stateProvider

		.state('app', {
			url: '/',
			views: {
				'header': {
					templateUrl: 'views/mainheader.html'
				},
				'content': {
					templateUrl: 'views/main.html',
					controller: 'recommenderController'
				}
			}
		})


	$urlRouterProvider.otherwise('/');
})
