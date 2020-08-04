
var app = angular.module('myApp', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
});

app.controller('myCtrl', ['$scope','$filter','$http','$sce', function ($scope, $filter,$http,$sce){
    $scope.registro = {};
    $scope.mensagens = [];
    
    $scope.enviarMensagem = function(){
        $http({
            url: "/api/mural", method:"POST", data: $scope.registro
        }).then(function(response) {
            console.log(response.data)
            $scope.pegaMensagens()
            $scope.messageBox("Show! tudo certo",response.data)
        },function(response){
            console.log(response.data)
            $scope.messageBox("Ops! algo deu errado",response.data)
        })
    }

    $scope.pegaMensagens = function(){
        $http({
            url: "/api/mural", method:"GET"
        }).then(function(response) {
            console.log(response.data)
            $scope.mensagens = response.data
        },function(response){
            console.log(response.data)
            $scope.messageBox("Ops! algo deu errado",response.data)
        })
    }



    $scope.deletar = function(registro){

        $scope.confirm = {"title":"Confirmação","message":"deseja deletar a mensagem?","func":function(){
            console.log({id:registro.id})
            $http({url: "/api/mural",
            method: "DELETE",
            data:{id:registro.id},
            headers: {"Content-Type": "application/json"}}).then(function(retorno){
                $scope.pegaMensagens()
                $("#modalyesno").modal("hide")
                $scope.messageBox("saida",retorno.data)
    
            },function(retorno){
                $("#modalyesno").modal("hide")
                $scope.messageBox("Ops! algo deu errado",retorno.data)
            })
        }}
        $("#modalyesno").modal("show")
    }


    $scope.messageBox = function(title,msg){
        $scope.msgbox = {"title":title,"message":msg}
        $("#msgbox").modal("show")
    }

    $scope.pegaMensagens()

}]);






