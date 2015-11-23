var app = angular.module('deepx', ['ui.bootstrap', 'ui.router', 'ngAnimate', 'angular-loading-bar',
                         'angulartics', 'angulartics.google.analytics']);

app.directive("deepxProject", function() {
  return {
    restrict: 'E',
    scope: '=',
    templateUrl: "/templates/deepx-project.html",
    link: function(scope, element, attrs) {
    }
  }
});
