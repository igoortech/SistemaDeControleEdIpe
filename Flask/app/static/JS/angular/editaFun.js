
var app = angular.module('myApp', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
});


app.controller('myCtrl', ['$scope','$filter','$http','$sce', function ($scope, $filter,$http,$sce){
    $scope.funcionarios = []
    $scope.funcselected = null

    $scope.pegafun = function(){
        $http({url: "/api/usuarios",method: "GET"
            }).then(function(response) {
                $scope.funcionarios = response.data
                console.log($scope.funcionarios)
            },function(response){
                $scope.messageBox("Algo Deu errado!", response.data)
            })

    }

    $scope.messageBox = function(title,msg){
        $scope.msgbox = {"title":title,"message":msg}
        $("#msgbox").modal("show")
    }


    $scope.seleciona_func = function (func) {
        $scope.funcselected = func
        $scope.old = angular.copy(func);

        $("#modal").modal("show")
    }


    $scope.status = function(func,sts){

        $http({url: "/api/status",method: "POST", data:{"id_ponto":func.id_ponto,status:sts}
            }).then(function(response) {
                $scope.messageBox("Sucesso!", response.data)
                $scope.pegafun()
            },function(response){
                $scope.messageBox("Algo Deu errado!", response.data)
            })
            $("#modalyesno").modal("hide")
    }


    $scope.messageBox = function(title,msg){
      $scope.msgbox = {"title":title,"message":msg}
      $("#msgbox").modal("show")
    }

    $scope.msg = function(msg,tipo){
        if (tipo){
            $scope.mensagem = $sce.trustAsHtml("<b>Show! tudo certo:</b><br/>" + msg)
            $scope.classmsg = 'alert-success'
        }else{
            $scope.mensagem = $sce.trustAsHtml("<b>Ops! algo deu errado:</b><br/>" + msg)
            $scope.classmsg = 'alert-danger'
        }
    }
  
    $scope.update = function (){
        $scope.mensagem  = null
        if($scope.old.senha !=  $scope.funcselected.senha){

            if ($scope.funcselected.senha != $scope.funcselected.senha2){
                $scope.msg("Campos de senha devem ser iguais!",false)
                $scope.pegafun()
                return
            }
            if ($scope.funcselected.senha.trim() == "" || $scope.funcselected.senha2.trim() == ""){
                $scope.msg("O campo senha é obrigatório!",false)
                $scope.pegafun()
                return
            }
        }
    
        $http({
            url: "/api/usuarios",
            method: "PUT",
            data:$scope.funcselected
        }).then(function(response) {
            $scope.msg(response.data,true)
        },function(response){
            $scope.msg(response.data,false)
        })
        
    
    
        }
    
    



        $scope.pegafun()

   }]);




