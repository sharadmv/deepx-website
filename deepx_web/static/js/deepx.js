var app = angular.module('deepx', ['ui.bootstrap', 'ui.router', 'ngAnimate', 'angular-loading-bar']);

app.directive("deepxProject", function() {
  return {
    restrict: 'E',
    scope: '=',
    templateUrl: "/templates/deepx-project.html",
    link: function(scope, element, attrs) {
    }
  }
});
