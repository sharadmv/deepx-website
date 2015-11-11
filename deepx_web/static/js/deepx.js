var app = angular.module('deepx', ['ui.bootstrap', 'ui.router', 'ngAnimate']);

app.directive("deepxProject", function() {
  return {
    restrict: 'E',
    scope: {
        project: "=project"
    },
    transclude: true,
    templateUrl: "/templates/deepx-project.html",
    link: function(scope, element, attrs) {
    }
  }
});

app.config(function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise("/home");
  $stateProvider.
    state('home', {
      url: "/home",
      templateUrl: '/templates/homepage.html',
      controller: 'HomeController'
    }).
    state('beermind', {
      url: "/beermind",
      templateUrl: '/templates/beermind.html',
      controller: 'BeermindController'
    })
});

app.controller('HomeController', function ($scope, $window) {
  $scope.beermind = {
    name: "BeerMind",
    href: "beermind",
    backgroundImage: "/img/coffee.jpg"
  }
});

app.controller('HomeCarouselController', function ($scope, $window) {
  $scope.interval = 5000;
  $scope.noWrapSlides = false;
  var slides = $scope.slides = [
    {
      image: '/img/space.jpg',
      text: 'Rethinking how machines learn'
    },
    {
      image: '/img/mountain-night.jpg',
      text: 'Redefining neural computation'
    },
    {
      image: '/img/mountains.jpg',
      text: 'Reaching new heights in scalability'
    },
    {
      image: '/img/nasa.jpg',
      text: 'Pushing the horizon of technology'
    },
  ];
});

app.controller('BeermindController', function ($scope, $window) {
  $scope.beermind = {
    name: "BeerMind",
    href: "beermind",
    backgroundImage: "/img/coffee.jpg"
  }
});
