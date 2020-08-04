
var app = angular.module('myApp', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
});


app.controller('myCtrl', ['$scope','$filter','$http','$sce', function ($scope, $filter,$http,$sce){
    $scope.prestadores = []
    $scope.prestador_selecionado = null
    

    $scope.atualizaPrincipal = function(){
        parametros = {url: "/api/prestadores",method: "GET"}
        $http(parametros).then(sucessoPrincipal,errorPrincipal)  
    }


    function sucessoPrincipal(response){
        console.log(response.data)
        $scope.prestadores = response.data
    }

    function errorPrincipal(response){
        console.log(response)
    }

    $scope.atualizaPrestador = function(){
        parametros = {url: "/api/alterar_prestador",method: "POST",data:$scope.prestador_selecionado} //Enviando o prestador alterado para a API atualizar no banco de dados

        $http(parametros).then(sucessoPrestador,errorPrestador)  
    }

    function sucessoPrestador(response){
        
        $('#modal').modal('hide')

    
        $scope.messageBox("Sucesso!",response.data)
          
       
    }

    function errorPrestador(response){
        $('#modal').modal('hide')
        $scope.messageBox("Erro!",response.data)
    }


    $scope.editar = function(prestador){
        $scope.prestador_selecionado = prestador
        $('#modal').modal('show') // mostrar o modal na tela
    }

    $scope.messageBox = function(title,msg){
        $scope.msgbox = {"title":title,"message":msg}
        $("#msgbox").modal("show")
    }



    $scope.carregaregistros = function(){
        $http({
            url: "/api/controle_acesso/pendentes",
            method: "GET",
        }).then(function(response) {
        console.log(response.data)
        $scope.todos = response.data
        },function(a){
            console.log(a)
        })  
    }





    $scope.atualizaPrincipal()
}]);






