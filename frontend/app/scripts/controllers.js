'use strict'
angular.module('recommenderApp')
.controller('recommenderController', function($scope, $http, $q, twitterService) {
    $scope.tweets = []; //array of tweets

    twitterService.initialize();

    //using the OAuth authorization result get the latest 20 tweets from twitter for the user
    $scope.refreshTimeline = function(maxId) {
        twitterService.getLatestTweets(maxId).then(function(data) {
            $scope.tweets = $scope.tweets.concat(data);
        }, function() {
            $scope.rateLimitError = true;
        });
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

                // twitterService.getLatestTweets().then(function(data) {
                //     var user_tweet;
                //     var tweet_list = [];
                //     user_tweet = data;
                //     // for(var i = 0; i < data.length; i++) {
                //     //     tweet_list[i] = data[i]["text"]
                //     // }
                twitterService.getUserInfo().then(function(data) {
                    var user_name = data["name"];
                    var userid = data["id"]
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
                        url: 'http://localhost:5000/influence/',
                        type: "get",
                        data: {"userid": userid}, 
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
                    // $scope.influence_list = [];
                    // $scope.influence_list = [];

                    // var list = [['CalvinHarris', 3533, 13259773], ['official_flo', 2343, 5566075], ['pitbull', 2670, 27111987], ['justinbieber', 315929, 105670945], ['kelly_clarkson', 86, 12447161], ['ladygaga', 127818, 77617421], ['JessicaSimpson', 240, 7294517], ['pattonoswalt', 2967, 4446505], ['WhitneyCummings', 569, 1278625], ['jimmykimmel', 598, 11267577], ['Maclifeofficial', 65, 59353], ['brendonwalsh', 982, 81601], ['adamraycomedy', 13042, 44521], ['TheNotoriousMMA', 546, 7078277], ['evan_breen', 572, 315047], ['chrisdelia', 852, 586243], ['billburr', 347, 1064292], ['toddbarry', 835, 317506], ['kbnoswag', 851, 76776], ['GaddorCole', 121, 12], ['John_Kavanagh', 406, 244314], ['SBG_Ireland', 99, 43040], ['RusHammerMMA', 393, 46182], ['BarackObama', 624049, 100998802], ['RedHourBen', 433, 6065036], ['jimmyfallon', 7821, 50717946], ['HillaryClinton', 772, 22096944], ['MichelleObama', 15, 10411264], ['FLOTUS', 5, 10087028], ['JordinSparks', 5556, 4178314], ['BrunoMars', 108, 41747624], ['KELLYROWLAND', 1712, 7261376], ['rihanna', 1116, 86625186]]
                    // var list_iter = []
                    // var flag = false

                    // for (var i = 0; i < $scope.list.length; i++) {
                    //     $scope.influence_list[i] = {
                    //         "name": $scope.list[i][0],
                    //         "iter": i,
                    //         "friends": $scope.list[i][2],
                    //         "followers": $scope.list[i][3]
                    //     }
                    // }
                    // console.log($scope.influence_list)

                    // for (var i = 0; i < $scope.list.length; i++) {
                    //     if ($scope.u_name == $scope.influence_list[i].name) {
                    //         $scope.u_rank = i + 1
                    //         flag = true
                    //         break
                    //     }
                    // } 
                    // if (flag == false) {
                    //     $scope.u_rank = $scope.list.length + 1
                    // }
                });

                // })

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
