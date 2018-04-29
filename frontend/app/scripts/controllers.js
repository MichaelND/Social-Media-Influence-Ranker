'use strict'
angular.module('recommenderApp')
.controller('recommenderController', function($scope, $http, $q, twitterService) {
    $scope.tweets = []; //array of tweets
    $scope.user_ids = []; //array of user ids
    $(document).ready(function(){
        $('.tabs').tabs();
        $("")
    });
    twitterService.initialize();

    //using the OAuth authorization result get the latest 20 tweets from twitter for the user
    $scope.refreshTimeline = function(maxId) {
        twitterService.getLatestTweets(maxId).then(function(data) {
            $scope.tweets = $scope.tweets.concat(data);
        }, function() {
            $scope.rateLimitError = true;
        });
    }

    //when the user adds a twitter id to a form
    $scope.addtolist = function() {
        var inputtext = document.getElementById('twitteruserid').value;
        console.log(inputtext);
        $scope.user_ids.push(inputtext);
        console.log($scope.user_ids);
    }
    //when the user decides when they want to submit the list to be ranked
    $scope.submitform = function() {
        console.log($scope.user_ids)
        $.ajax({
            url: 'http://127.0.0.1:5000/sort',
            type: "get",
            // contentType: 'application/json',
            crossDomain: true,
            data: {"userids": JSON.stringify($scope.user_ids)}, 
            success: function(response) {
                $scope.$apply(function() {
                    console.log(response)
                    $scope.influence_list = response["influence_list"];
                })
            },
            error: function(xhr, err, errmsg) {
                console.log(errmsg)
            }
        })
    }

    //when the user clicks the connect twitter button, the popup authorization window opens
    $scope.connectButton = function() {
        twitterService.connectTwitter().then(function() {
            if (twitterService.isReady()) {
                //if the authorization is successful, hide the connect button and display the tweets
                $('#connectButton').fadeOut(function() {
                    $('#signOut').fadeIn();
                    $('#results').fadeIn();
                    $scope.connectedTwitter = true;
                });
                twitterService.getUserInfo().then(function(data) {
                    var user_name = data["screen_name"];
                    $scope.u_name = data["screen_name"]
                    $scope.u_friends = data["friends_count"]
                    $scope.u_followers = data["followers_count"]
                    $scope.u_rank = 0
                    // console.log(data["screen_name"])
                    // for (var i = 0; i < user_tweet.length; i++) {
                    //     tweet_list.push({
                    //         "content": user_tweet[i]["text"],
                    //         "contenttype": "text/plain",
                    //         "created": 1447639154000,
                    //         "id": user_tweet[i]["id"],
                    //         "language": "en",
                    //         "sourceid": "Twitter API",
                    //         "userid": user_name
                    //     })
                    // }
                    // user_tweet = angular.toJson(tweet_list)
    
                    $.ajax({
                        url: 'http://127.0.0.1:5000/influence',
                        type: "get",
                        data: {"userid": user_name}, 
                        success: function(response) {
                            $scope.$apply(function() {
                                console.log(response)
                                $scope.influence_list = response["influence_list"];
                            })
                        },
                        error: function(xhr, err, errmsg) {
                            console.log(errmsg)
                        }
                    })
                });

            } else {

            }
        });
    }

    //sign out clears the OAuth cache, the user will have to reauthenticate when returning
    $scope.signOut = function() {
        twitterService.clearCache();
        $scope.tweets.length = 0;
        $scope.influence_list = []
        $('#signOut').fadeOut(function() {
            $('#connectButton').fadeIn();
            $('#results').fadeOut();
            $scope.$apply(function() {
                $scope.connectedTwitter = false
            })
        });
    }

    //if the user is a returning user, hide the sign in button and display the tweets
    if (twitterService.isReady()) {
        $('#connectButton').hide();
        $('#signOut').show();
        $scope.connectedTwitter = true;
    }
});