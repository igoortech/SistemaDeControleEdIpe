
var app = angular.module('myApp', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
});

function contains(a, obj) {
    var i = a.length;

    while (i--) {
        if (a[i] == obj) {
            return true;

        }

    }
    return false;
}

app.filter('unique', function () { //--------------------------- retira duplicatas no campo

    var i = 0;

    var x = function (original, filtro,filtro2) {
        var valor = 0;
        var itens2 = [];
        var itens = [];

        for (i = 0; i < original.length; i++) {
            if (!contains(itens2, original[i][filtro][filtro2])) {
                itens2.push(original[i][filtro][filtro2]);
                itens.push(original[i]);
            }
        }
        return itens;
    };
    return x;
});

app.filter('uniqueDate', function () { //--------------------------- retira duplicatas no campo

    var i = 0;

    var x = function (original, filtro) {
        var valor = 0;
        var itens2 = [];
        var itens = [];

        for (i = 0; i < original.length; i++) {
            if (!contains(itens2, original[i][filtro])) {
                itens2.push(original[i][filtro]);
                itens.push(original[i]);
            }
        }
        return itens;
    };
    return x;
});

app.filter('filterJson', function () {

    var x = function (original, campo,valor) {
        if(valor == undefined){
            return original
        }
        lst = original.filter(function(a){if(a[campo] == valor){return a[campo]}})
        return lst;
    };
    return x;
});



app.controller('myCtrl', ['$scope','$filter','$http','$sce', function ($scope, $filter,$http,$sce){

   $scope.registro_ponto = []
   $scope.funcionarios = []
   $scope.confirm = null

   $scope.pega_ponto = function () {

        $http({
            url: "/api/ponto",
            method: "GET",
        }).then(function(response) {
        console.log(response.data)
        $scope.registro_ponto = response.data
        },function(response){
            $scope.messageBox("Algo Deu errado!", "Não foi possível carregar os dados")
        })  

   }


    $scope.messageBox = function(title,msg){
        $scope.msgbox = {"title":title,"message":msg}
        $("#msgbox").modal("show")

    }

    $scope.saida_a = function(linha){
        $scope.confirm = {"title":"Confirmação","message":"confirmar saída para almoço?","func":function(){
            $scope.enviaPonto("saida_a")
        }}
        $("#modalyesno").modal("show")
    }
    $scope.volta_a = function(linha){
        $scope.confirm = {"title":"Confirmação","message":"confirmar a volta do almoço?","func":function(){
            $scope.enviaPonto("volta_a")
        }}
        $("#modalyesno").modal("show")
    }
    $scope.saida = function(linha){
        $scope.confirm = {"title":"Confirmação","message":"confirmar saída?","func":function(){
            $scope.enviaPonto("saida")
        }}
        $("#modalyesno").modal("show")
    }

    $scope.enviaPonto = function(tipo){
        $http({url: "/api/ponto",method: "POST", data:{"tipo":tipo}
            }).then(function(response) {
                $scope.messageBox("Sucesso!", response.data)
                $scope.pega_ponto()
            },function(response){
                $scope.messageBox("Algo Deu errado!", response.data)
            })
            $("#modalyesno").modal("hide")
    }

    //$("#modalyesno").modal("show")

    $scope.pega_ponto()

   }]);




