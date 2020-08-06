
var app = angular.module('myApp', [], function($interpolateProvider) {
            $interpolateProvider.startSymbol('[{');
            $interpolateProvider.endSymbol('}]');
  });


app.controller('myCtrl', ['$scope','$filter','$http','$sce', function ($scope, $filter,$http,$sce){


    $scope.atividades = []
    $scope.prestadores = []
    $scope.documento = ""
    $scope.destinos = ['Ed.Ipê',101,102,103,104,201,202,203,204,301,302,303,304,401,402,403,404,501,502,503,504,601,602,603,604,701,702,703,704,801,802,803,804,901,902,903,904,1001,1002,1003]
    $scope.confirm = null
  

    
    




    $scope.atualizaPrincipal = function(){
        $http({
            url: "/api/controle_acesso/pendentes",
            method: "GET",
        }).then(function(response) {
        console.log(response.data)
        $scope.atividades = response.data
        },function(a){
            console.log(a)
        })  
    }

    $scope.atualizaPrestadores = function(){
        $http({
            url: "/api/prestadores",
            method: "GET",
        }).then(function(response) {
        console.log(response.data)
        $scope.prestadores = response.data
        },function(a){
            console.log(a)
        })
    }


    $scope.add = function(){
        $scope.mensagem = null

        prestador = $scope.prestadores.filter(function(a){if(a['doc'] == $scope.documento){return a['doc']}})

        if( prestador.length > 0){
            if($scope.destinoSelecionado != ""){
                dados = {"Documento":$scope.documento,"Destino":$scope.destinoSelecionado}

                $http({url: "/api/add_registro",method: "POST",data:dados}).then(function(retorno){
                    $scope.atualizaPrincipal()
                    $scope.documento = null
                    $scope.destinoSelecionado = ""
                    $scope.msg("Entrada cadastrada com sucesso!",true)
                    //$("#modal").modal('hide')

                },function(retorno){
                    $scope.msg(retorno.data,false)
                })
            }else{
                $scope.msg("Selecione um destino!",false)
            }
            
        }else{
            $scope.msg("Prestador nao encontrado na base de dados!",false)
        }


        $scope.documento
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

    $scope.messageBox = function(title,msg){
        $scope.msgbox = {"title":title,"message":msg}
        $("#msgbox").modal("show")
    }

    $scope.darSaida = function(registro){

        $scope.confirm = {"title":"Confirmação","message":"deseja dar saída?","func":function(){

            $http({url: "/api/darsaida",method: "POST",data:{"id_controle_acesso":registro.id}}).then(function(retorno){
                $scope.atualizaPrincipal()
                $("#modalyesno").modal("hide")
                $scope.messageBox("saida","Saída realizada com sucesso!")
    
            },function(retorno){
                $scope.msg(retorno.data,false)
            })
        }}
        $("#modalyesno").modal("show")
    }

  
    $scope.atualizaPrincipal()
    $scope.atualizaPrestadores()
}]);


app.filter('filterJson', function () {

    var x = function (original, campo,valor) {
        lst = original.filter(function(a){if(a[campo] == valor){return a[campo]}})
        return lst;
    };
    return x;
});



