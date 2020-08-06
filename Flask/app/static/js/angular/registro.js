
var app = angular.module('myApp', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
});

app.filter('filterJson', function () {

    var x = function (original, campo,valor,contains) {
        if(valor == undefined){
            return original
        }
        if(contains){
            lst = original.filter(function(a){if(a[campo].includes(valor)){return a[campo]}})
        }else{
            lst = original.filter(function(a){if(a[campo] == valor){return a[campo]}})
        }
        
        return lst;
    };
    return x;
});

app.controller('myCtrl', ['$scope','$filter','$http','$sce', function ($scope, $filter,$http,$sce){
    $scope.todos = []
    $scope.funcionarios = []
    $scope.prestadores = []
    $scope.destinos = ['Ed.Ipê',101,102,103,104,201,202,203,204,301,302,303,304,401,402,403,404,501,502,503,504,601,602,603,604,701,702,703,704,801,802,803,804,901,902,903,904,1001,1002,1003]
    $scope.selectedReg = {}
 

    $scope.carregaregistros = function(){
        parametros = {url: "/api/controle_acesso/todos",method: "GET"}
        $http(parametros).then(sucessoRegistros,errorRegistros)  
    }

    $scope.pega_usuarios = function () {
        $scope.mensagem = null
        $http({
            url: "/api/usuarios",
            method: "GET",
        }).then(function(response) {
        console.log(response.data)
        $scope.funcionarios = response.data
        },function(response){
            $scope.messageBox("Algo Deu errado!", "Não foi possível carregar os dados")
        })  
    
    }
    $scope.pega_prestadores = function () {
        $scope.mensagem = null
        $http({
            url: "/api/prestadores",
            method: "GET",
        }).then(function(response) {
        console.log(response.data)
        $scope.prestadores = response.data
        },function(response){
            $scope.messageBox("Algo Deu errado!", "Não foi possível carregar os dados")
        })  
    
    }

    $scope.excluir = function () {
        $scope.mensagem = null
        $http({
            url: "/api/controle_acesso",
            method: "DELETE",
            data: {'id_reg':$scope.selectedReg.id},
            headers: {"Content-Type": "application/json"} //mandando para api um dicionario
        }).then(function(response) {
        console.log(response.data)
            $scope.msg(response.data,true)
            $scope.carregaregistros()
        },function(response){
            $scope.msg(response.data,false)
        })  
    
    }


    $scope.alteraRegistro = function () {
        $scope.mensagem = null
        $scope.selectedReg.id_prestador = $scope.selectedReg.prestador.id
        $scope.selectedReg.id_ponto_e = $scope.selectedReg.user_entrada.id_ponto
        $scope.selectedReg.id_ponto_s = $scope.selectedReg.user_saida.id_ponto

        $http({
            url: "/api/controle_acesso",
            method: "PUT",
            data: $scope.selectedReg
        }).then(function(response) {
        console.log(response.data)
        $scope.msg(response.data,true)
        $scope.carregaregistros()
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


    function sucessoRegistros(response){
        console.log(response.data)
        $scope.todos = response.data
    }

    function errorRegistros(response){
        console.log(response)
    }


    $scope.selecionaRegistro = function (registro) {
        $scope.mensagem = null
        $scope.selectedReg = registro
        $scope.selectedReg.user_entrada = $scope.funcionarios.filter(function(item){if(item.id_ponto == registro.user_entrada.id_ponto){return item}})[0]
        $scope.selectedReg.user_saida = $scope.funcionarios.filter(function(item){if(item.id_ponto == registro.user_saida.id_ponto){return item}})[0]
        $scope.selectedReg.prestador = $scope.prestadores.filter(function(item){if(item.id == registro.id_prestador){return item}})[0]
        $("#modal").modal("show")
    }



    $scope.carregaregistros()
    $scope.pega_usuarios()
    $scope.pega_prestadores()
}]);






