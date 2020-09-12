// used https://www.twilio.com/blog/2018/03/video-chat-react.html for help

var AccessToken = require('twilio').jwt.AccessToken;
var VideoGrant = AccessToken.VideoGrant;
var app = express();

// Endpoint to generate access token
app.get('/token', function(request, response) {
    var identity = faker.name.findName();
 
    // Create an access token which we will sign and return to the client,
    // containing the grant we just created
    var envToken = new AccessToken(
        process.env.TWILIO_ACCOUNT_SID,
        process.env.TWILIO_API_KEY,
        process.env.TWILIO_API_SECRET
    );
 
    // Assign the generated identity to the token
    envToken.identity = identity;
 
    const grant = new VideoGrant();
    // Grant token access to the Video API features
    envToken.addGrant(grant);
 
    // Serialize the token to a JWT string and include it in a JSON response
    response.send({
        identity: identity,
        token: envToken.toJwt()
    });
 });

 var port = process.env.PORT || 3000;

