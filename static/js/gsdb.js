
$('.datePicker').datepicker();
var host = 'http://localhost:5000/rest/api/1/'
var app = angular.module('gsdbApp', []);
var page_key = $('#page_key').val();

app.controller('listCtrl', ['$scope', '$http', function($scope, $http){
    $scope.sortType = 'rank';
    $scope.sortReverse = false;
    $http.get(host + page_key)
    .success(function(data){
        alertZeroData(data);
        $scope.tops = [data[0], data[1], data[2]];
        $scope.users = data.slice(3, data.length);
    })
    .error(function(){
        alert("시스템 서버 에러!!");
    });
}]);

app.controller('searchCtrl', ['$scope', '$http', function($scope, $http){
    $scope.search = function(start, end){
        if(typeof(start) != "undefined" && typeof(end)!= "undefined"){
            if(new Date(start) < new Date(end)){
            data: JSON.stringify({
                            's_m': start.split('/')[0],
                            's_d': start.split('/')[1],
                            's_y': start.split('/')[2],
                            'e_m': end.split('/')[0],
                            'e_d': end.split('/')[1],
                            'e_y': end.split('/')[2]
                        });
                $http.post(host + page_key + '/search', data)
                .success(function(data){
                    alertZeroData(data);
                    $scope.tops = [data[0], data[1], data[2]];
                    $scope.users = data.slice(3, data.length);
                }).error(function(){
                    alert("system error!!");
                });
            }
            else {
                alert("시작 날짜와 끝 날짜가 맞지 않습니다.");
            }
        }
        else {
            alert("날짜를 입력해주세요");
        }
    };
}]);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});


function alertZeroData(data){
    if(data[0][1] == "0"){
        alert("값이 모두 0입니다. 순위는 무관합니다.");
    };
};
