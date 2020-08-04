
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

app.filter('uniqueMes', function () { //--------------------------- retira duplicatas no campo

    var i = 0;
    var x = function (original, filtro) {
        var valor = 0;
        var itens2 = [];
        var itens = [];

        for (i = 0; i < original.length; i++) {
            if (!contains(itens2, original[i][filtro].split("/")[1])) {
                itens2.push(original[i][filtro].split("/")[1]);
                itens.push(original[i].h_entradaf.split('/')[1]);
            }
        }
        return itens;
    };
    return x;
});

app.filter('uniqueAno', function () { //--------------------------- retira duplicatas no campo

    var i = 0;
    var x = function (original, filtro) {
        var valor = 0;
        var itens2 = [];
        var itens = [];

        for (i = 0; i < original.length; i++) {
            if (!contains(itens2, original[i][filtro].split("/")[2].split(" ")[0])) {
                itens2.push(original[i][filtro].split("/")[2].split(" ")[0]);
                itens.push(original[i].h_entradaf.split('/')[2].split(' ')[0]);
            }
        }
        return itens;
    };
    return x;
});

app.filter('filterMes', function () {

    var x = function (original, campo,valor) {
        if(valor == undefined){
            return original
        }
        valor = "/" + valor +  "/"
        lst = original.filter(function(a){if(a[campo].includes(valor)){return a[campo]}})
        return lst;
    };
    return x;
});

app.filter('filterAno', function () {

    var x = function (original, campo,valor) {
        if(valor == undefined){
            return original
        }
        valor = "/" + valor
        lst = original.filter(function(a){if(a[campo].includes(valor)){return a[campo]}})
        return lst;
    };
    return x;
});

app.controller('myCtrl', ['$scope','$filter','$http','$sce', function ($scope, $filter,$http,$sce){
    $scope.funcionarios_list = []
    $scope.funSelected = null
    $scope.funActivies = []

    
    
    $scope.visualizar = function (x) {
        $scope.funSelected = x
        $scope.funActivies = []

        $http({
            url: "/api/user_atividades/" +$scope.funSelected.id_ponto, method:"GET",
        }).then(function(response) {
        console.log(response.data)
        $scope.msg(response.data,true)
        $scope.funActivies = response.data
        },function(response){
            console.log(response.data)
            $scope.msg(response.data,false)
        })  

        $("#modal").modal("show")

    }
  
    

    $scope.pega_atividades = function () {


        $http({
            url: "/api/prestadores",
            method: "GET",
        }).then(function(response) {
        console.log(response.data)
        $scope.msg(response.data,true)
        $scope.funcionarios_list = response.data

        },function(response){
            $scope.msg(response.data,false)
        })  
    }
    
    $scope.pega_funcs = function () {
        
        $http({
            url: "/api/usuarios",
            method: "GET",
        }).then(function(response) {
        console.log(response.data)
        $scope.msg(response.data,true)
        $scope.funcionarios_list = response.data
        },function(response){
            $scope.msg(response.data,false)
        })  

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


    $scope.pega_funcs()


   
}]);






