// used https://www.twilio.com/blog/2018/03/video-chat-react.html

import React, { Component } from 'react';
import Video from 'twilio-video';
import axios from 'axios';
import { Button } from 'reactstrap';
import TextField from '@material-ui/core/TextField';

// When this loads, componentDidMount makes API call to server and gets a token.
// This token is how the user can join rooms so the token info will be stored in state.

export default class Performance extends Component {
 constructor(props) {
   super();
   this.state = {
       identity: null,
       roomName: '',
       roomNameError: false, // allows us to show a nice error message if there is a problem
       localMediaAvailable: false, // assume no connected video/audio?
       hasJoinedRoom: false,
       localTrack: null,
       joinedRoom: null // keep track of the active, joined room 
    }
    this.joinPerformance = this.joinPerformance.bind(this);
    this.updateRoomNameChange = this.updateRoomNameChange.bind(this);
    this.performanceJoined = this.performanceJoined.bind(this);
    this.leavePerformance = this.leavePerformance.bind(this);
    //this.detachParticipantTracks = this.detachParticipantTracks(this);
 }

 componentDidMount() {
     // make the API call to get the token and update state accordingly
     axios.get('/token').then(results => {
        const { identity, token } = results.data;
        this.setState({ identity, token });
    });
 }

 updateRoomNameChange(e){
    this.setState({
        roomName: e.target.value,
    });
 }

 joinPerformance(){
    // display nice message if no room name was entered (or was just whitespace)
    if(this.state.roomName.trim().length === 0){
        this.setState({
            roomNameError: true,
        });
        return;
    }

    console.log("Joining the performance: '" + this.state.roomName + "'! ");
    let joiningOptions = {
        name: this.state.roomName,
    };

    if(this.state.localTrack){
        joiningOptions.tracks = this.state.localTrack
    }

    const AccessToken = require('twilio').jwt.AccessToken;
    const VideoGrant = AccessToken.VideoGrant;

    var identity = this.state.identity;

    const videoGrant = new VideoGrant({
        room: this.state.roomName,
    });

    const token = new AccessToken(
        process.env.REACT_APP_TWILIO_ACCOUNT_SID,
        process.env.REACT_APP_TWILIO_API_KEY,
        process.env.REACT_APP_TWILIO_API_SECRET);
    token.addGrant(videoGrant);
    token.identity = identity;

    // connect to the performance!
    Video.connect(token.toJwt(), joiningOptions).then(this.performanceJoined, error => {
        alert('Could not connect to Twilio: ' + error.message);
    });
 }

// Attach the Tracks to the DOM.
attachTracks(tracks, container) {
    tracks.forEach(track => {
      container.appendChild(track.attach());
    });
  }
  
  // Attach the Participant's Tracks to the DOM.
  attachParticipantTracks(participant, container) {
    var tracks = Array.from(participant.tracks.values());
    this.attachTracks(tracks, container);
  }
 
  // Detach Tracks
  detachTracks(tracks) {
    tracks.forEach(track => {
      track.detach().forEach(detachedElement => {
        detachedElement.remove();
      });
    });
  }

 // detachParticipantTracks(participant) {
 //   var tracks = Array.from(participant.tracks.values());
 //   this.detachTracks(tracks);
 // }
  
  performanceJoined(room) {
    // Called when a participant joins a room
    console.log("Joined as '" + this.state.identity + "'");
    this.setState({
      activeRoom: room,
      localMediaAvailable: true,
      hasJoinedRoom: true  // Removes ‘Join Room’ button and shows ‘Leave Room’
    });
  
    // Attach LocalParticipant's tracks to the DOM, if not already attached.
    var previewContainer = this.refs.localMedia;
    if (!previewContainer.querySelector('video')) {
      this.attachParticipantTracks(room.localParticipant, previewContainer);
    }

    // TODO: Add performer's tracks
    // TODO: Add any friends' tracks
    // this.attachParticipantTracks(participant, this.refs.remoteMedia)

    // Attach participant's tracks if they are with friends
    room.on('trackAdded', (track, participant) => {
        var previewContainer = this.refs.remoteMedia;
        this.attachTracks([track], previewContainer);
      });
     
    // If they remove a track, detach it
    room.on('trackRemoved', (track, participant) => {
        this.detachTracks([track]);
    });

    // If disconnect, detatch tracks
    room.on('participantDisconnected', participant => {
        this.detachParticipantTracks(participant);
    });

    room.on('disconnected', () => {
        if (this.state.previewTracks) {
          this.state.previewTracks.forEach(track => {
            track.stop();
          });
        }
        this.detachParticipantTracks(room.localParticipant);
        room.participants.forEach(this.detachParticipantTracks);
        this.state.activeRoom = null;
        this.setState({ hasJoinedRoom: false, localMediaAvailable: false });
    });
  }

  leavePerformance(){
        this.state.activeRoom.disconnect();
        this.setState({
            hasJoinedRoom: false,
            localMedia: false,
        });
  }

 render() {
        /* 
    Controls showing of the local track
    Only show video track after user has joined a room else show nothing 
    */
    let localTrack = this.state.localMediaAvailable ? (
        <div className="flex-item"><div ref="localMedia" /> </div>) : '';   
    /*
    Controls showing of ‘Join Room’ or ‘Leave Room’ button.  
    Hide 'Join Room' button if user has already joined a room otherwise 
    show `Leave Room` button.
    */
    let joinOrLeaveRoomButton = this.state.hasJoinedRoom ? (
    <Button secondary={true} onClick={this.leavePerformance}>Leave Performance </Button> ) : (
    <Button primary={"true"} onClick={this.joinPerformance}>Join Performance</Button>);
    return (
        <div>
            <div>Performance</div>
            <div>
            <div className="flex-container">
            {localTrack} {/* Show local track if available */}
            <div className="flex-item">
            {/* 
            The following text field is used to enter a room name. It calls  `handleRoomNameChange` method when the text changes which sets the `roomName` variable initialized in the state.
            */}
                <p>Performance Room: </p>
                <TextField hinttext="Room Name" onChange={this.updateRoomNameChange} 
                    errortext = {this.state.roomNameError ? 'Room Name is required' : undefined} 
                /><br />
                {joinOrLeaveRoomButton}  {/* Show either ‘Leave Room’ or ‘Join Room’ button */}
            </div>
            {/* 
            The following div element shows all remote media (other                             participant’s tracks) 
            */}
            <div className="flex-item" ref="remoteMedia" id="remote-media" />
            </div>
            </div>
        </div>
        );
    }
}