
var app = angular.module('myApp', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
});


app.controller('myCtrl', ['$scope','$filter','$http','$sce','$window', function ($scope, $filter,$http,$sce,$window){
  $scope.campos ={}


  $scope.messageBox = function(title,msg){
    $scope.msgbox = {"title":title,"message":msg}
    $("#msgbox").modal("show")
  }

  $scope.cadastra = function (){
    
    if ($scope.campos.senha != $scope.campos.senha2){
        $scope.messageBox("Algo errado!", "Campos de senha devem ser iguais!")
        return
    }
    if ($scope.campos.senha.trim() == "" || $scope.campos.senha2.trim() == ""){
        $scope.messageBox("Algo errado!", "O campo senha é obrigatório!")
        return
    }

    $http({
        url: "/api/usuarios",
        method: "POST",
        data:$scope.campos
    }).then(function(response) {
        $scope.messageBox("Cadastrado realizado!!",response.data)
        $scope.campos ={}
        $window.location.href = '/func';
        
    },function(response){
        $scope.messageBox("Algo errado!",response.data)
    })
    


  }



}]);






