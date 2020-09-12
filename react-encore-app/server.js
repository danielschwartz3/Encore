// used https://www.twilio.com/blog/2018/03/video-chat-react.html for help

var AccessToken = require('twilio').jwt.AccessToken;
var VideoGrant = AccessToken.VideoGrant;
var app = express();

// Endpoint to generate access token
app.get('/token', function(request, response) {
    // Until we connect profiles and this, generate fake name
    var identity = faker.name.findName();
 
    // Create an access token which we will sign and return to the client,
    // containing the grant we just created
    var token = new AccessToken(
        process.env.REACT_APP_TWILIO_ACCOUNT_SID,
        process.env.REACT_APP_TWILIO_API_KEY,
        process.env.REACT_APP_TWILIO_API_SECRET
    );
    token.identity = identity;
    // Grant token access to the Video API features
    const grant = new VideoGrant();
    token.addGrant(grant);
    token = token.toJwt();
    // Serialize the token to a JWT string and include it in a JSON response
    response.send({
        identity: identity,
        token: token.toJwt(),
    });
 });

 var port = process.env.PORT || 3000;

