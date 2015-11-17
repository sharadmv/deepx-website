app.config(function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise("/home/main");
  $stateProvider.
    state('splash', {
      url: "/",
      templateUrl: '/templates/splash.html',
      controller: 'SplashController'
    }).
    state('home', {
      url: "/home",
      templateUrl: '/templates/layout.html',
    }).
    state('home.main', {
      url: "/main",
      templateUrl: '/templates/homepage.html',
      controller: 'HomeController'
    }).
    state('home.beermind', {
      url: "/beermind",
      templateUrl: '/templates/beermind.html',
      controller: 'BeermindController'
    }).
    state('home.papers', {
      url: "/papers",
      templateUrl: '/templates/papers.html',
      controller: 'PapersController'
    })
});
