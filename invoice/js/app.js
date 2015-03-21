angular.module("MyApp", [])
    .controller("MyController",function($scope,MyService){

        $scope.test="Test";
        $scope.konner = "";
       
        $scope.nameInput ='';
        $scope.ageInput='';
        
        $scope.employeeArray = MyService.getItems();

        $scope.addItem = function(){

       
            if ($scope.nameInput.length,$scope.ageInput.length) {
            var newEmp = {};
            newEmp.name = $scope.nameInput;
            newEmp.age = $scope.ageInput;
            MyService.addItem(newEmp);
        }else{
            alert("enter something");
        }

            $scope.nameInput ='';
            $scope.ageInput='';


        };

        $scope.removeItem = function(idx){
            MyService.removeItemAt(idx)
        }


    })

    .service("MyService",function(){

        var items=[];

        this.getItems = function(){

            var lsData = localStorage.getItem('MyLocalData');

            items = JSON.parse(lsData) || items;

            return items;
        };

        this.addItem = function(itemObject){
            items.push(itemObject);
          

            var stringyData = JSON.stringify(items);
            localStorage.setItem('MyLocalData',stringyData)


        };


        this.removeItemAt = function(itemIndex){
            items.splice(itemIndex,1);

            var stringyData = JSON.stringify(items);
            localStorage.setItem('MyLocalData',stringyData)
        }

    });
