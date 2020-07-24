
var app = angular.module('myApp', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
});


app.controller('myCtrl', ['$scope','$filter','$http','$sce', function ($scope, $filter,$http,$sce){
    $scope.todos = []

 

    $scope.carregaregistros = function(){
        parametros = {url: "/api/controle_acesso/todos",method: "GET"}
        $http(parametros).then(sucessoRegistros,errorRegistros)  
    }


    function sucessoRegistros(response){
        console.log(response.data)
        $scope.todos = response.data
    }

    function errorRegistros(response){
        console.log(response)
    }



    $scope.carregaregistros()
}]);






