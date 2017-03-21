app.config(function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise("/home/main");
  $stateProvider.
    state('splash', {
      url: "/splash",
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
    state('home.ddc', {
      url: "/ddc",
      controller: 'DDCController'
    }).
    state('home.about', {
      url: "/about",
      templateUrl: '/templates/about.html',
      controller: 'AboutController'
    }).
    state('home.software', {
      url: "/software",
      templateUrl: '/templates/software.html',
      controller: 'SoftwareController'
    }).
    state('home.papers', {
      url: "/papers",
      templateUrl: '/templates/papers.html',
      controller: 'PapersController'
    })
});
